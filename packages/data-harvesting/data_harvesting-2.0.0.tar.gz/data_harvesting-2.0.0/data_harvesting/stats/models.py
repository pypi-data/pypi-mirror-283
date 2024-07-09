# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Tuple, List
import re


@dataclass
class LogData:
    """Class to store log data."""

    request_method: str
    request_url: str
    status_code: int
    request_time: int
    domain_name: str
    report_item_name: str

    def to_tuple(self) -> Tuple[str, str, int, int, str, str]:
        return (
            self.request_method,
            self.request_url,
            self.status_code,
            self.request_time,
            self.domain_name,
            self.report_item_name,
        )


@dataclass
class ReportItem:
    """Class to store report items. Each report item has a unique name."""

    name: str  # should be unique
    domain_name: str
    url_patterns: List[str]  # regex

    def url_matches(self, domain_name: str, request_url: str) -> bool:
        if domain_name != self.domain_name:
            return False

        for pattern in self.url_patterns:
            if re.match(pattern, request_url):
                return True
        return False
