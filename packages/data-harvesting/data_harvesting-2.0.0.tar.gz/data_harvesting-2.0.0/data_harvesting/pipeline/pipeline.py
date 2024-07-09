# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
This module contains all the files and util concerning prefect and the data pipeline
"""
from pathlib import Path
from typing import Optional

from prefect import flow
from prefect import get_run_logger
from prefect.client.schemas.schedules import CronSchedule
from prefect.deployments import Deployment
from prefect.infrastructure import Process
from .aggregator import run_aggregator
from .harvester import run_harvester
from .indexer import run_indexer
from .uploader import run_uploader
from data_harvesting import get_config
from data_harvesting.harvester import HARVESTER_CLASSMAP as harvester_classmap


def register_pipeline(
    time_interval: str = '0 0 * * SAT',
    harvester: str = 'all',
    out: Optional[Path] = None,
    config: Optional[Path] = None,
    uplifting=True,
    index=True,
    upload=True,
    label: str = '',
):
    """Register the pipeline flow runs as a cron job in prefect.

    you can test the pipeline run by parsing (replace with now)
    --time_interval '30 12 05 06 *'
    bzw {minute} {hour} {day} {month} *'
    """
    cron_schedule = CronSchedule(cron=time_interval, timezone='Europe/Berlin')

    cron_deploy = Deployment(
        name=f'pipeline-deployment{label}',
        flow_name=f'Run-data-pipeline-{harvester}-uplift-{uplifting}-index-{index}-upload-{upload}-interval_{time_interval}',
        entrypoint='data_harvesting/pipeline/pipeline.py:run_pipeline',
        parameters={'harvester': harvester, 'out': out, 'config': config, 'uplifting': uplifting, 'index': index, 'upload': upload},
        schedules=[cron_schedule],
        work_queue_name='default',
        path='/usr/src',
        infrastructure=Process(type='process', stream_output=True),
    )

    cron_deploy.apply()


@flow(log_prints=True, flow_run_name='pipe-{harvester}-uplift-{uplifting}-index-{index}-upload-{upload}')
def run_pipeline(
    harvester: str = 'all',
    out: Optional[Path] = None,
    config: Optional[Path] = None,
    uplifting=True,
    index=True,
    upload=True,
):
    """
    A prefect flow to run a single or all harvesters
    """
    logger = get_run_logger()
    logger.info('Data pipeline start')
    # Todo implement conditional failures...
    if harvester == 'all':
        # rekursion
        # read config, only run pipeline for Harvesters present
        config_full = get_config(config)
        config_harvester_list = list(config_full.keys())
        for harvester_key, harvester_val in list(harvester_classmap.items()):
            if harvester_val.__name__ in config_harvester_list:
                if config_full.get(harvester_val.__name__, None) is not None:
                    run_pipeline(
                        harvester=harvester_key,
                        out=out,
                        config=config,
                        uplifting=uplifting,
                        upload=upload,
                        index=index,
                    )
    else:
        # we do not submit these subflows, we run them, because they depend on each other.
        harvested_list = run_harvester(harvester=harvester, out=out, config=config)  # .result(raise_on_failure=False)
        nfiles = len(harvested_list)
        # logger.info(f'Harvested_list {harvested_list}')
        logger.info(f'Harvested {nfiles} files')

        if uplifting:
            if len(harvested_list) > 0:
                run_aggregator(harvested_list, config=config, source=harvester, nfiles=nfiles)  # , wait_for=harvested_list)
            else:
                logger.info('Skipping Aggregator subflow, because list with files to uplift is empty.')
        if index:
            if len(harvested_list) > 0:
                run_indexer(harvested_list, config=config, source=harvester, nfiles=nfiles)
            else:
                logger.info('Skipping indexer subflow, because list with files to index is empty.')
        if upload:
            if len(harvested_list) > 0:
                failures = run_uploader(harvested_list, source=harvester, config=config, nfiles=nfiles)
                nfailes = len(failures)
                if nfailes > 0:
                    logger.info('Uploading subflow finished with {nfails} failures.')
            else:
                logger.info('Skipping uploader subflow, because list with files to upload is empty.')
    logger.info('Data pipeline end!')
