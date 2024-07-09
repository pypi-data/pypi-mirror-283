# -*- coding: utf-8 -*-
from prefect.client.schemas.schedules import CronSchedule
from prefect.deployments import Deployment
from data_harvesting.stats.config import DEBUG
from datetime import datetime, timedelta
from prefect.infrastructure import Process


POOL_NAME = 'test-pool'


def register_flows():
    """Register the nginx log collection flow as a cron job in prefect."""
    now = datetime.now()
    now_2 = now + timedelta(minutes=2)
    now_4 = now + timedelta(minutes=4)
    daily_cron_debug = f'{now_2.minute} {now_2.hour} {now_2.day} {now_2.month} *'
    weekly_cron_debug = f'{now_4.minute} {now_4.hour} {now_4.day} {now_4.month} *'

    daily_cron = daily_cron_debug if DEBUG else '0 0 * * *'
    weekly_cron = weekly_cron_debug if DEBUG else '0 0 * * SUN'

    daily_schedule = CronSchedule(cron=daily_cron, timezone='Europe/Berlin')
    weekly_schedule = CronSchedule(cron=weekly_cron, timezone='Europe/Berlin')

    daily_deploy = Deployment(
        name='daily-deployment',
        flow_name='Record Nginx logs',
        entrypoint='data_harvesting/stats/record/flow.py:save_logs',
        schedules=[daily_schedule],
        work_queue_name='default',
        path='/usr/src',
        infrastructure=Process(type='process', stream_output=True),
    )

    weekly_deploy = Deployment(
        name='weekly-deployment',
        flow_name='Report Nginx logs',
        entrypoint='data_harvesting/stats/report/flow.py:report_logs',
        schedules=[weekly_schedule],
        work_queue_name='default',
        path='/usr/src',
        infrastructure=Process(type='process', stream_output=True),
    )

    daily_deploy.apply()
    weekly_deploy.apply()
