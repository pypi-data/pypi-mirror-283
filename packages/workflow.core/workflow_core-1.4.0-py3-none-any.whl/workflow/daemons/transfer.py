"""Workflow Transfer Daemon."""

import time
from typing import Any, Dict, List, Union

import click
from click_params import JSON, URL, FirstOf
from workflow import DEFAULT_WORKSPACE_PATH
from workflow.http.buckets import Buckets
from workflow.http.results import Results
from workflow.utils.logger import get_logger
from workflow.utils import read
from workflow.lifecycle import configure
from workflow.http.context import HTTPContext

logger = get_logger("workflow.daemons.transfer")


def deposit_work_to_results(
    buckets: Buckets, results: Results, works: List[Dict[str, Any]]
) -> int:
    """Deposit work to results, and remove them from buckets.

    Args:
        buckets (Buckets): Buckets module.
        results (Results): Results module.
        works (List[Dict[str, Any]]): Work to deposit.

    Returns:
        transfer_status (bool): Number of works deposited to results.
    """
    try:
        transfer_status = False
        results_deposit_status = results.deposit(works)
        if all([val > 0 for val in results_deposit_status.values()]):
            buckets.delete_ids([work["id"] for work in works])
            transfer_status = True
        return transfer_status
    except Exception as error:
        print(f"Exception occurred: {error}")
        transfer_status = False
        work_to_deposit = [
            work for work in works if is_work_already_deposited(results, work) is False
        ]
        results_deposit_status = results.deposit(work_to_deposit)
        if (
            all([val > 0 for val in results_deposit_status.values()])
            or results_deposit_status == {}
        ):
            buckets.delete_ids([work["id"] for work in works])
            transfer_status = True
        return transfer_status


def is_work_already_deposited(results: Results, work: Dict[str, Any]) -> bool:
    """Check if a work has already been deposited to results.

    Args:
        results (Results): Results module.
        work (Dict[str, Any]): work to check

    Returns:
        bool: _description_
    """
    return results.count(pipeline=work["pipeline"], query={"id": work["id"]}) == 1


@click.command()
@click.option("--sleep", "-s", default=5, help="seconds to sleep between transfers.")
@click.option(
    "-w",
    "--workspace",
    type=FirstOf(
        click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
        URL,
        JSON,
    ),
    default=(DEFAULT_WORKSPACE_PATH.as_posix()),
    show_default=True,
    help="workspace config.",
)
@click.option("--limit", default=50, help="works to transfer per run.")
@click.option(
    "--cutoff", default=60 * 60 * 24 * 7, help="cutoff time in seconds for stale work."
)
@click.option(
    "--test-mode", default=False, help="Enable test mode to avoid while True loop"
)
def transfer(
    sleep: int,
    workspace: Union[str, Dict[Any, Any]],
    test_mode: bool,
    limit: int,
    cutoff: int,
) -> Dict[str, Any]:
    """Transfer work from Buckets to Results.
    Args:
        sleep (int): seconds to sleep between transfers.
        workspace (Union[str, Dict[Any, Any]]): workspace config.
        test_mode (bool): Enable test mode to avoid while True loop.
        limit (int): works to transfer per run.
        cutoff (int): cutoff time in seconds for stale work.

    Returns:
        Dict[str, Any]: _description_
    """
    logger.info("Starting Transfer Daemon")
    logger.info(f"Sleep Time: {sleep}")
    logger.info(f"Workspace : {workspace}")
    logger.info(f"Test Mode : {test_mode}")
    logger.info(f"Limit/Tx  : {limit}")
    logger.info(f"Cutoff    : {cutoff} days")
    configure.workspace(workspace=workspace)
    archive: bool = (
        read.workspace(DEFAULT_WORKSPACE_PATH.as_posix())
        .get("config", {})
        .get("archive", {})
        .get("results", True)
    )
    logger.info(f"Archive   : {'Enabled' if archive else 'Disabled'}")
    http: HTTPContext = HTTPContext(backends=["buckets", "results"])
    logger.info("HTTP Context Initialized")
    logger.info(f"HTTP Context: Buckets Backend @ {http.buckets.baseurl}")
    logger.info(f"HTTP Context: Results Backend @ {http.results.baseurl}")

    delete: List[str] = []
    successful: List[Dict[str, Any]] = []
    failed: List[Dict[str, Any]] = []

    for work in http.buckets.view(
        query={"status": "success"}, projection={}, skip=0, limit=limit
    ):
        if work["config"]["archive"]["results"] is False:
            delete.append(work["id"])
        elif work["config"]["archive"]["results"] is True and archive:
            successful.append(work)
        else:
            delete.append(work["id"])

    # Transfer successful work to results
    response: Dict[str, Any] = {}
    response = http.results.deposit(successful)
    for key, value in response.items():
        if value:
            delete.append(key)
    
    try:
        logger.info(f"Transferring {len(successful)} successful works to results")
        response = http.results.deposit(successful)
        for key, value in response.items():
            if value:
                delete.append(key)
    except Exception as error:
        logger.error("Failed to deposit successful works to results")
        logger.error(f"Exception: {error}")
        

    def transfer(test_flag: bool, buckets: Buckets, results: Results) -> Dict[str, Any]:
        """Transfer Work from Buckets to Results.

        Args:
            test_flag (bool): If True, run once and exit.
            buckets (Buckets): Buckets module.
            results (Results): Results module.

        Returns:
            Dict[str, Any]: Transfer status.
        """

        transfer_status: Dict[str, Any] = {}
        # 1. Transfer successful Work
        # TODO: decide projection fields
        successful_work = buckets.view(
            query={"status": "success"},
            projection={},
            skip=0,
            limit=limit,
        )
        successful_work_to_delete = [
            work
            for work in successful_work
            if work["config"]["archive"]["results"] is False
            and not results_workspace_config
        ]
        successful_work_to_transfer = [
            work
            for work in successful_work
            if work["config"]["archive"]["results"] is True and results_workspace_config
        ]

        if successful_work_to_transfer:
            transfer_status["successful_work_transferred"] = deposit_work_to_results(
                buckets, results, successful_work_to_transfer
            )
        if successful_work_to_delete:
            buckets.delete_ids([work["id"] for work in successful_work_to_delete])
            transfer_status["successful_work_deleted"] = True

        cutoff_creation_time = time.time() - (60 * 60 * 24 * 7)
        # 2. Transfer failed Work which is not stale
        failed_work = buckets.view(
            query={
                "status": "failure",
                "$expr": {"$gte": ["$attempt", "$retries"]},
                "creation": {"$gt": cutoff_creation_time},
            },
            projection={},
            skip=0,
            limit=limit,
        )
        failed_work_to_delete = [
            work
            for work in failed_work
            if work["config"]["archive"]["results"] is False
            and not results_workspace_config
        ]
        failed_work_to_transfer = [
            work
            for work in failed_work
            if work["config"]["archive"]["results"] is True and results_workspace_config
        ]

        if failed_work_to_transfer:
            transfer_status["failed_work_transferred"] = deposit_work_to_results(
                buckets, results, failed_work_to_transfer
            )
        if failed_work_to_delete:
            buckets.delete_ids([work["id"] for work in failed_work_to_delete])
            transfer_status["failed_work_deleted"] = True

        # 3. Delete stale Work (cut off time: 7 days)
        stale_work = buckets.view(
            query={
                "status": "failure",
                "creation": {"$lt": cutoff_creation_time},
            },
            projection={},
            skip=0,
            limit=limit,
        )
        if stale_work:
            buckets.delete_ids([work["id"] for work in stale_work])
            transfer_status["stale_work_deleted"] = True
        log.info(f"Transfer Status: {transfer_status}")
        return transfer_status

    if test_mode:
        return transfer(test_flag=True, buckets=buckets, results=results)
    while True:
        transfer(test_flag=False, buckets=buckets, results=results)
        time.sleep(sleep)


if __name__ == "__main__":
    transfer()
