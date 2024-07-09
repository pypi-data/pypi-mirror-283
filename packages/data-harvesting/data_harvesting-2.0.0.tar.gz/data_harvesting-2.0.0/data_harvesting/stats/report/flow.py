# -*- coding: utf-8 -*-
from typing import List, Tuple
from data_harvesting.stats.config import REPORT_ITEMS, REPORT_FILE, GIT_FOLDER
from data_harvesting.stats.models import LogData
from data_harvesting.stats.database.operations import get_weekly_data
from prefect import flow, task, get_run_logger
from datetime import datetime
from data_harvesting.stats.report.git import commit_and_push, clone_repository
from shutil import rmtree


def print_rows(rows: List[LogData]):
    if not rows or not isinstance(rows, list) or len(rows) == 0:
        return
    logger = get_run_logger()

    # log report item name
    logger.debug(f'Report Item: {rows[0].report_item_name}\n')
    # print the column names
    columns = ['Request Method', 'Request URL', 'Status Code', 'Request Time', 'Domain Name']
    logger.debug(' | '.join(columns))
    logger.debug('-' * 100)
    for row in rows:
        logger.debug(' | '.join([str(cell) for cell in row.to_tuple()[:-1]]))
    logger.debug('\n\n')


@task(persist_result=True, log_prints=True, task_run_name='save-csv-{time}')
def save_csv(data: List[Tuple[str, int]], time: datetime = datetime.now()):
    """Save the data to a CSV file.

    Args:
        data (List[Tuple[str, int]]): The data to save.
    """
    logger = get_run_logger()

    if not data or not isinstance(data, list) or len(data) == 0:
        logger.info('No data to save.')
        return

    logger.info('Saving data to CSV file.')

    if not REPORT_FILE.is_file():
        # create the CSV file with the column names
        REPORT_FILE.write_text(f"Date,{','.join(item[0] for item in data)}\n")

    with open(REPORT_FILE, 'a') as f:
        time_str = time.strftime('%Y-%m-%d')
        f.write(f"{time_str},{','.join(str(item[1]) for item in data)}\n")


@flow(name='Report Nginx Logs', log_prints=True, persist_result=True, flow_run_name='report_nginx_logs')
def report_logs():
    """Report the Nginx logs."""
    logger = get_run_logger()
    logger.info('Reporting Nginx logs.')

    data = []
    for report_item in REPORT_ITEMS:
        rows = get_weekly_data(report_item.name)
        print_rows(rows)
        data.append((report_item.name, len(rows)))

    # delete the GIT folder if it exists to clone the latest repository
    if GIT_FOLDER.exists():
        rmtree(GIT_FOLDER, ignore_errors=True)

    clone_repository()

    save_csv(data)

    commit_and_push()
