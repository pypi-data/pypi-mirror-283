# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
This module contains all the flows for the indexer.
"""
import json
import progressbar
from pathlib import Path
from typing import List
from typing import Optional

from prefect import flow
from prefect import get_run_logger

from data_harvesting.indexer import Indexer
from data_harvesting.util.map_ror import ROR_SCHEMA_DATA_PATH  # get_ror_schemadata_by_id


@flow(log_prints=True, flow_run_name='index-{source}-nrecords-{nfiles}')
def run_indexer(
    files: List,
    config: Optional[Path] = None,
    source: str = 'non-specified',
    nfiles: int = -1,
    fl_reindex: bool = False,
    fail: bool = False,
    enhance_ror: bool = True,
    pbar: bool = True,
):
    """
    A prefect flow to run the indexer
    """
    nfiles = len(files)
    logger = get_run_logger()
    logger.info(f'Indexer start on {nfiles} records from source {source}!')
    indexer = Indexer(conf=config, since=None)
    indexer_conf = indexer.config
    logger.info(f'Indexing with config: {indexer_conf}')
    if pbar:
        prbar = progressbar.ProgressBar(max_value=nfiles, redirect_stdout=True)
    for i, file_ in enumerate(files):
        if pbar:
            prbar.update(i)
        # logger.info('Indexing Data source: %s', str(file_))
        indexer.index_file(file_, unhidedata=True, fail=fail, fl_reindex=fl_reindex, since=None)
    logger.info(f'Indexer finished on {nfiles} records!')

    # Post index better data for ROR ids.
    # this might still lead to overwrite of good rich ror data with lesser, due to a twofold child
    # parent relationships. without cutting one...
    if enhance_ror:
        ror_ids = indexer.ror_ids
        # reimplementation of get_ror_schemadata_by_id(ror_id) # to make this faster
        # by opening the file once

        ror_data_file = ROR_SCHEMA_DATA_PATH
        if ror_data_file.exists():
            logger.info(f'Indexer post indexing {len(ror_ids)} ror ids!')
            with open(ror_data_file, 'r', encoding='utf-8') as stream:
                data = json.load(stream)
            for ror_id in ror_ids:
                ror_schema_org = data.get(ror_id, None)
                if ror_schema_org is not None:
                    indexer.index_data(ror_schema_org, fail=fail, fl_reindex=fl_reindex)
        else:
            logger.warning(f'Could not enhance ROR data, since file: {ror_data_file} does not exists.')
