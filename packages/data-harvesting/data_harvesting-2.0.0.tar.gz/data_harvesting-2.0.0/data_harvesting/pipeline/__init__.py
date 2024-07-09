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
# prefect has a problem with its poetry installation, only works nicely with pip install prefect
# What should be come a flow
# A single pipeline should run for one harvester source only
# each provider source should be come its own sub pipeline? or only sub task in each step
#
import os

from .aggregator import run_aggregator
from .harvester import run_harvester
from .indexer import run_indexer
from .pipeline import run_pipeline
from .uploader import run_uploader

# enable logging of lib
os.environ['PREFECT_LOGGING_EXTRA_LOGGERS'] = 'data_harvesting,data-harvesting'

__all__ = ['run_aggregator', 'run_harvester', 'run_indexer', 'run_pipeline', 'run_uploader']
