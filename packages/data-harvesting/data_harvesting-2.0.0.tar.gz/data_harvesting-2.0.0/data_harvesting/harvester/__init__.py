# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""Module which contains all harvesters"""
from typing import Dict
from typing import Type

from data_harvesting.harvester.base import BaseHarvester
from data_harvesting.harvester.datacite import DataciteHarvester
from data_harvesting.harvester.feed import FeedHarvester
from data_harvesting.harvester.git import GitHarvester
from data_harvesting.harvester.indico import IndicoHarvester
from data_harvesting.harvester.oaipmh.oai import OAIHarvester
from data_harvesting.harvester.sitemap import SitemapHarvester


# Better would probably be to register Harvesters over entry points.
HARVESTER_CLASSMAP: Dict[str, Type[BaseHarvester]] = {
    'git': GitHarvester,
    'sitemap': SitemapHarvester,
    'datacite': DataciteHarvester,
    'oai': OAIHarvester,
    'indico': IndicoHarvester,
    'feed': FeedHarvester,
}
__all__ = [
    'HARVESTER_CLASSMAP',
    'BaseHarvester',
    'HarvesterMetadata',
    'DataciteHarvester',
    'FeedHarvester',
    'GitHarvester',
    'IndicoHarvester',
    'OAIHarvester',
    'SitemapHarvester',
]
