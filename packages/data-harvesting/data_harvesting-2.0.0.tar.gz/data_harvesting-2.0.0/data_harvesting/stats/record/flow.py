# -*- coding: utf-8 -*-
from prefect import flow, get_run_logger
from data_harvesting.stats.database.operations import get_last_request_time, insert_log
from data_harvesting.stats.record.utils import parse_log_line
from pathlib import Path
from data_harvesting.stats.config import LOG_PATH
from data_harvesting.stats.database.setup import create_db


@flow(name='Record Nginx logs', log_prints=True, persist_result=True, flow_run_name='record_nginx_logs')
def save_logs():
    logger = get_run_logger()
    # Create the database if it doesn't exist
    create_db()

    # check if log file exists
    if not Path(LOG_PATH).exists() or not Path(LOG_PATH).is_file():
        logger.error('Nginx log file not found.')
        return

    last_request = get_last_request_time()

    # Read log file line by line
    logger.info('Reading nginx log file...')
    with open(LOG_PATH) as f:
        for line in f:
            log_data = parse_log_line(line)
            if not log_data:
                continue
            # only insert log data that is newer than the last request
            if log_data.request_time > last_request:
                insert_log(log_data)

    logger.info('Nginx log data saved to database.')
