# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""Module containing the Base Harvester class"""
import logging
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

from pydantic import ConfigDict, HttpUrl
from data_harvesting import get_config
from data_harvesting import get_config_path
from data_harvesting.data_model import LDOMetadata


class HarvesterMetadata(LDOMetadata):
    """Metadata for linked data object harvested by an unhide harvester."""

    model_config = ConfigDict(extra='forbid')

    # NOTE: all fields are only used by some of the harvesters... :(

    # either all possible fields should be listed and well-defined,
    # or model_config should set extra='allow' to add arbitrary things
    # (but first option is better, otherwise one can also just use plain dict again)
    harvester_class: Optional[str] = None
    source_pid: Optional[str] = None
    provider: Optional[str] = None
    preprocess: Optional[str] = None
    sitemap: Optional[HttpUrl] = None
    git_url: Optional[HttpUrl] = None
    endpoint: Optional[HttpUrl] = None


logger = logging.getLogger(__name__)


class BaseHarvester(ABC):
    """Basic harvester class template to be implemented for a given pipeline

    Required in a method called run.
    It also stores a list with pointers to harvested Objects during its lifetime
    This class may be extended in the future with maybe functions to parse
    and process data
    """

    outpath: Path = Path('.')  #
    config: dict  #  Configuration of the harvester
    sources: dict  # Data provider sources to harvest from
    last_harvest: List[Path]  # Pointers to linkedDataObjects, if different storage backend, change this.
    successes: List[str]  # successful harvested records pids
    failures: List[str]  # failed to harvest record pids in some way
    last_harvest_dump_path: Path  # Path the last harvest file was dumped

    def __init__(self, outpath=Path('.'), config_path=get_config_path()):
        """Initialize the Harvester

        Outpath: where data will be stored
        config_path: Path to the config files to read sources
        """
        self.outpath = outpath
        self.set_config(config_path=config_path)
        self.last_harvest = []
        self.failures = []
        self.successes = []

    def set_config(self, config_path=get_config_path()):
        """Set sources and harvester specific config from a given config"""
        full_config = get_config(config_path)

        # This is the harvester specific part in the config
        self.config = full_config.get(self.__class__.__name__, {})
        self.sources = self.config.get('sources', {})

    def get_sources(self) -> dict:
        """Return sources"""
        return self.sources

    def get_config(self) -> dict:
        """Return harvester specific config"""
        return self.config

    def get_last_harvest_dump_path(self) -> Optional[Path]:
        """Return path to last harvest file, if set"""
        return self.last_harvest_dump_path

    def get_successes(self) -> List[str]:
        """Return list of successes from last harvester run"""
        return self.successes

    def get_failures(self) -> List[str]:
        """Return list of successes from last harvester run"""
        return self.failures

    @abstractmethod
    def run(
        self,
        *,
        source: str = 'all',
        since: Optional[datetime] = None,
        base_savepath: Path = outpath,
    ) -> None:
        """Run the harvester
        This method is required to be implemented for every harvester
        """
        raise NotImplementedError

    def get_last_run_file(self, source: Optional[str] = None) -> Path:
        """Get location of file where timestamp of last run of harvester for given out dir is stored."""
        harvester = self.__class__.__name__
        source = source or 'all'
        file_name = f'{harvester}.{source}.last_run'
        return self.outpath / file_name

    def set_last_run(self, source: str, time: Optional[datetime] = datetime.now()) -> None:
        """
        Saves the last run time of the harvester to a file.
        May be overwritten by each harvester.
        """
        last_run_file = self.get_last_run_file(source)
        print(last_run_file)

        with open(last_run_file, 'w', encoding='utf-8') as file:
            file_content = time.strftime('%Y-%m-%d %H:%M:%S') if time else ''
            file.write(file_content)

    def get_last_run(self, source: Optional[str] = None) -> Optional[datetime]:
        """
        Get the last run time of the harvester as datetime.
        May be overwritten by each harvester.
        """
        last_run_file = self.get_last_run_file(source=source)
        if not last_run_file.is_file():
            return None

        try:
            with open(last_run_file, 'r', encoding='utf-8') as file:
                date = file.read().strip('\n')
                return datetime.strptime(date, '%Y-%m-%d %H:%M:%S') if date else None
        except ValueError as exc:
            logging.error('Error, while reading last run file %s. %s', last_run_file, exc)

    def append_last_harvest(self, harvested_res: List[Path]) -> None:
        """Store Pointers to Objects harvested in execution of the class, append"""
        last_harvest = self.last_harvest or []
        last_harvest.extend(harvested_res)
        self.last_harvest = last_harvest

    def append_failures(self, failures: List[str]) -> None:
        """Store Pointers to records failed in the harvesting"""
        failures_ = self.failures or []
        failures_.extend(failures)
        self.failures = failures_

    def append_successes(self, successes: List[str]) -> None:
        """Store Pointers to records failed in the harvesting"""
        successes_ = self.successes or []
        successes_.extend(successes)
        self.successes = successes_

    def dump_last_harvest(self, target: Optional[Union[Path, str]] = None, source: Optional[str] = None):
        """Dump last harvest to a given_file"""
        harvester = self.__class__.__name__
        if source is None:
            file_name = f'{harvester}_Harvester_last_harvest.txt'
        else:
            file_name = f'{harvester}_{source}_Harvester_last_harvest.txt'
        dump_path = Path(f'{self.outpath}') / file_name
        if isinstance(target, str):
            target = Path(target)
        target = target or Path('.').joinpath(dump_path)
        self.last_harvest_dump_path = target  # .resolve() # at this point target has to be a Path
        with open(target, 'w', encoding='utf-8') as fileo:
            for pointer in self.last_harvest:
                fileo.write(str(pointer) + '\n')


# ToDO this kind of doubled functionality to harvester.__init__ HARVESTER_CLASSMAP
# decide on what we need.
class Harvesters(str, Enum):
    """Enum containing all supported harvesters"""

    GIT = 'GitHarvester'
    SITEMAP = 'SitemapHarvester'
    DATACITE = 'DataciteHarvester'
    OAI = 'OAIHarvester'
