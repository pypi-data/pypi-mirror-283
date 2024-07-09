# -*- coding: utf-8 -*-
from data_harvesting.stats.record.flow import save_logs
from data_harvesting.stats.report.flow import report_logs
from data_harvesting.stats.deployment import register_flows

all = [save_logs, report_logs, register_flows]
