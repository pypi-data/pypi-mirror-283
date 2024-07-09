# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
This module contains all the flows for the aggregator
"""

import progressbar
from pathlib import Path
from typing import List
from typing import Optional

from prefect import flow
from prefect import get_run_logger
from data_harvesting.util.data_model_util import apply_aggregator
from data_harvesting.util.config import get_config


@flow(log_prints=True, flow_run_name='uplift-{source}-nrecords-{nfiles}')
def run_aggregator(
    files: List,
    source: str = 'non-specified',
    nfiles: int = -1,
    config: Optional[Path] = None,
    dest: Optional[Path] = None,
    pbar: bool = True,
):
    """
    A prefect flow to run a single or all harvesters
    """
    nfiles = len(files)
    logger = get_run_logger()
    full_config = get_config(config)
    agg_conf = full_config.get('Aggregator', None)
    logger.info(f'Aggregator start on {nfiles} records using config: {agg_conf}!')
    overwrite = False
    if dest is None:
        overwrite = True
    if pbar:
        prbar = progressbar.ProgressBar(max_value=nfiles, redirect_stdout=True)
    for i, file_ in enumerate(files):
        # logger.info(f'Aggregate File: {file_}')
        if pbar:
            prbar.update(i)
        apply_aggregator(file_, config=config, overwrite=overwrite, dest=dest)
    logger.info(f'Aggregator finished uplifting {nfiles} records!')
