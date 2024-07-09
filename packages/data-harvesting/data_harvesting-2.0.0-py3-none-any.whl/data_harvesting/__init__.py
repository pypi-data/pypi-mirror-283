# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""This is the data-harvesting package. Containing:.

Set of tools to harvest, process and uplift (meta)data from metadata providers
within the Helmholtz association to be included in the Helmholtz Knowledge Graph
(Helmholtz-KG). The harvested linked data in the form of schema.org jsonld is
aggregated and uplifted in data pipelines to be included into a single large
knowledge graph (KG). The tool set and harvesters can be used as a python
library or over a commandline interface (CLI, hmc-unhide). Provenance of
metadata changes is tracked rudimentary by saving graph patches of changes on
rdflib Graph data structures on the semantic triple level. Harvesters support
extracting data via sitemap, gitlab API, datacite API and OAI-PMH endpoints.
"""
import importlib_metadata
import logging

from .util.config import get_config_path
from .util.config import get_config
from .aggregator import Aggregator
from .data_model import LinkedDataObject
from .rdfpatch import RDFPatch
from .indexer import Indexer

# create logging for module, all sub modules log to this
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logging.basicConfig(
    filename='data_harvesting.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# create console handler with formatter and add to logger
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)


__version__: str = importlib_metadata.version(__package__ or __name__)
__all__ = ['get_config_path', 'get_config', 'Aggregator', 'LinkedDataObject', 'RDFPatch', 'Indexer', 'logger']
