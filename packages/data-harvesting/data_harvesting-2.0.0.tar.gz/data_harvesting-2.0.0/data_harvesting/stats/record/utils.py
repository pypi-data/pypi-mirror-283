# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional
import re
from data_harvesting.stats.models import LogData
from data_harvesting.stats.report import get_report_item


def parse_log_line(log_line: str) -> Optional[LogData]:
    # $host $remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" "$upstream_addr"
    pattern = r'(?P<host>\S+)\s+(?P<remote_addr>\S+)\s+-\s+(?P<remote_user>\S+)\s+\[(?P<time_local>[^\]]+)\]\s+"(?P<request_method>[A-Z]+)\s+(?P<request_url>[^"]+)"\s+(?P<status>\d+)\s+(?P<body_bytes_sent>\d+)\s+"(?P<http_referer>[^"]+)"\s+"(?P<http_user_agent>[^"]+)"\s+"(?P<upstream_addr>[^"]+)"'

    match = re.match(pattern, log_line)
    if match:
        domain_name = match.group('host')
        timestamp_str = match.group('time_local')
        request_method = match.group('request_method')
        request_url = match.group('request_url').split(' ')[0]
        status_code_str = match.group('status')
        try:
            status_code = int(status_code_str)
        except ValueError:
            status_code = 0
        # Convert timestamp to Unix timestamp
        timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z')
        unix_timestamp = int(timestamp.timestamp())
        report_item = get_report_item(domain_name, request_url)
        if report_item is None:
            return None
        return LogData(
            request_method,
            request_url,
            status_code,
            unix_timestamp,
            domain_name,
            report_item.name,
        )
    else:
        return None
