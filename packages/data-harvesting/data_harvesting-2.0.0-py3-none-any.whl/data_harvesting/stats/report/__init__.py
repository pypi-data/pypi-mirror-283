# -*- coding: utf-8 -*-
from data_harvesting.stats.models import ReportItem
from typing import Optional
from data_harvesting.stats.config import REPORT_ITEMS


def get_report_item(domain_name: str, request_url: str) -> Optional[ReportItem]:
    for item in REPORT_ITEMS:
        if item.url_matches(domain_name, request_url):
            return item
    return None
