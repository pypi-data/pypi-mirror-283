# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
This module contains all the flows and tasks for the indexer
"""
import progressbar
from typing import List
from typing import Optional
from pathlib import Path
from prefect import flow
from prefect import get_run_logger

from data_harvesting.util.data_model_util import upload_data_filepath
from data_harvesting.util.config import get_config


@flow(log_prints=True, flow_run_name='upload-{source}-nrecords-{nfiles}-to-{endpoint_url}')
def run_uploader(
    files: List,
    source: str = 'non-specified',
    config: Optional[Path] = None,
    nfiles: int = -1,
    infrmt: str = 'json',
    graph_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    username: Optional[str] = None,
    passwd: Optional[str] = None,
    pbar: bool = True,
) -> list:
    """
    A prefect flow to upload a list of resources, which are in this case a List of file names.
    """
    total_failures = []
    nfiles = len(files)
    logger = get_run_logger()
    logger.info(f'Uploader start on {nfiles} records!')

    conf_dict = get_config(config)  # full
    conf_con_upload = conf_dict.get('Uploader', {}) or {}

    # parsed values go over environment variables set or settings from the config
    graph_name = graph_name or conf_con_upload.get('graph_name', None)
    endpoint_url = endpoint_url or conf_con_upload.get('endpoint_url', None)
    username = username or conf_con_upload.get('username', None)
    passwd = passwd or conf_con_upload.get('passwd', None)
    logger.info(f'Uploading with config: {conf_con_upload}')
    if pbar:
        prbar = progressbar.ProgressBar(max_value=nfiles, redirect_stdout=True)
    for i, file_ in enumerate(files):
        logger.info(f'Uploading File: {file_}')
        if pbar:
            prbar.update(i)
        failures = upload_data_filepath(
            file_, infrmt=infrmt, graph_name=graph_name, endpoint_url=endpoint_url, username=username, passwd=passwd
        )
        total_failures.extend(failures)
    logger.info(f'Uploader finished on {nfiles} records!')
    logger.info(f'Upload failed on {len(total_failures)} records!')
    return total_failures
