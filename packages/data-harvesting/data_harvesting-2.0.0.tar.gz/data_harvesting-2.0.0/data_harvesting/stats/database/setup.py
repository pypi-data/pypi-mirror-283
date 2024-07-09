# -*- coding: utf-8 -*-
import sqlite3
from data_harvesting.stats.config import DB_NAME


def create_db():
    """Create the database if it doesn't exist."""

    # create parent directory if it doesn't exist
    DB_NAME.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_NAME))
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS access_logs (request_method TEXT, request_url TEXT, status_code INTEGER, request_time INTEGER, domain_name TEXT, report_item_name TEXT)'
    )
    conn.commit()
    conn.close()
