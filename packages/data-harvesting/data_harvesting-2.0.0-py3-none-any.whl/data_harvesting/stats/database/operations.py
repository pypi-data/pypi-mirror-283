# -*- coding: utf-8 -*-
import sqlite3
from data_harvesting.stats.config import DB_NAME
from data_harvesting.stats.models import LogData
from datetime import datetime, timedelta
from typing import List, Optional


def insert_log(log_data: LogData):
    """Insert log data into the database.

    Args:
        log_data (LogData): Log data to insert into the database.
    """
    conn = sqlite3.connect(DB_NAME.resolve())
    c = conn.cursor()
    c.execute('INSERT INTO access_logs VALUES (?, ?, ?, ?, ?, ?)', log_data.to_tuple())
    conn.commit()
    conn.close()


def get_weekly_data(report_item_name: str, time: Optional[datetime] = None) -> List[LogData]:
    """Get the weekly data from the database.

    Args:
        report_item_name (str): The name of the report item to get the weekly data for.
        time (Optional[datetime], optional): The time to get the weekly data for, starts from exactly 1 week before. Defaults to None.

    Returns:
        List[LogData]: The weekly data from the database.
    """
    if time is None:
        time = datetime.now()

    conn = sqlite3.connect(DB_NAME.resolve())
    c = conn.cursor()
    c.execute(
        'SELECT * FROM access_logs WHERE request_time >= ? AND request_time <= ? AND report_item_name = ?',
        (int((time - timedelta(weeks=1)).timestamp()), int(time.timestamp()), report_item_name),
    )
    data = c.fetchall()
    conn.close()

    return [LogData(*row) for row in data]


def get_last_request_time() -> int:
    """Get the last request time from the database.

    Returns:
        int: The last request time from the database, 0 if empty.
    """
    conn = sqlite3.connect(DB_NAME.resolve())
    c = conn.cursor()
    # last row in the table is the latest request
    c.execute('SELECT MAX(request_time) FROM access_logs')
    last_time = c.fetchone()[0]
    conn.close()
    if last_time is None:
        return 0
    return int(last_time)
