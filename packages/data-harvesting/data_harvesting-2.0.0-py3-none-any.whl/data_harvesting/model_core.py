# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
Module containing general Data model and configuration the unhide projects needs.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, SecretStr, AnyUrl, ValidationInfo, field_validator
from typing import Optional, List, Dict, Literal, Any
from typing_extensions import Annotated
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class UnhideBaseModel(BaseModel):
    """Configured pydantic base model for unhide."""

    model_config = ConfigDict(validate_assignment=True, validate_default=True, populate_by_name=True)


class ProcessMetadata(UnhideBaseModel):
    """Administrative/technical metadata attached to objects by unhide processes.

    Subclass to add context-dependent extra fields (with suitable defaults if possible).
    """

    created_at: datetime = Field(default_factory=lambda: datetime.now())
    uuid: UUID = Field(default_factory=uuid4)


EP_REGEX = r'([^\d\W]\w*\.)*([^\d\W]\w*):([^\d\W]\w*)'
EntryPointStr = Annotated[str, Field(pattern=EP_REGEX)]
"""String looking like a Python entrypoint, i.e. `module.submodule.subsubmodule:object.subobj`."""


class AggregatorStackItem(UnhideBaseModel):
    """Model for a single Stack item for the Aggregator stack."""

    type: Literal['python', 'sparql']

    # for python update
    method: Optional[EntryPointStr] = None
    args_: Optional[List[Any]] = Field(default_factory=lambda: [], alias='args')
    kwargs_: Optional[Dict[str, Any]] = Field(default_factory=lambda: {}, alias='kwargs')

    # for sparql update
    file: Optional[Path] = None


class AggregatorConfig(UnhideBaseModel):
    """Model for the config part the Aggregator can process."""

    stack: List[AggregatorStackItem] = []


class HarvesterSourceBaseModel(UnhideBaseModel):
    """Base model for all Harvester config parts"""

    name: str


class UrlTransform(UnhideBaseModel):
    replace: List[str]


class SitemapHarvesterSourceItem(HarvesterSourceBaseModel):
    """Model for the an entry of the configuration of the SitemapHarvester"""

    url: str
    match_pattern: Optional[str] = None
    url_transforms: Optional[List[UrlTransform]] = None
    replace: Optional[List[str]] = None


class SitemapHarvesterConfig(UnhideBaseModel):
    """Model for the configuration of the SitemapHarvester"""

    sources: Dict[str, List[SitemapHarvesterSourceItem]] = {}


class GitHarvesterGitlabItem(HarvesterSourceBaseModel):
    """Model for the an entry of the configuration of the GitHarvester"""

    url: str


# class GitHarvesterSourceItem(UnhideBaseModel):
#    List[GitHarvesterGitlabItem]


class GitHarvesterConfig(UnhideBaseModel):
    """Model for the configuration of the GitHarvester"""

    sources: Dict[str, List[GitHarvesterGitlabItem]] = {}


class OAIHarvesterConfigSourceItem(HarvesterSourceBaseModel):
    """Model for the an entry of the configuration of the OAIHarvester"""

    oai_endpoint: str
    convert: Optional[bool] = True
    metadataPrefix: Optional[str] = 'oai_dc'


class OAIHarvesterConfig(UnhideBaseModel):
    """Model for the configuration of the OAIHarvester"""

    sources: Dict[str, OAIHarvesterConfigSourceItem] = {}


class DataciteHarvesterSourceItem(HarvesterSourceBaseModel):
    """Model for the an entry of the configuration of the DataciteHarvester"""

    ror: str
    follow_children: Optional[bool] = None


class DataciteHarvesterConfig(UnhideBaseModel):
    """Model for the configuration of the DataciteHarvester"""

    sources: Dict[str, DataciteHarvesterSourceItem] = {}


class IndicoHarvesterSourceItem(UnhideBaseModel):
    """Model for the an entry of the configuration of the IndicoHarvester"""

    categories: List[int] = []
    url: str
    token: Optional[str] = None


class IndicoHarvesterConfig(UnhideBaseModel):
    """Model for the configuration of the IndicoHarvester"""

    sources: Dict[str, IndicoHarvesterSourceItem] = {}


class FeedHarvesterSourceItem(UnhideBaseModel):
    """Model for the an entry of the configuration of the FeedHarvester"""

    urls: List[str]


class FeedHarvesterConfig(UnhideBaseModel):
    """Model for the configuration of the FeedHarvester"""

    sources: Dict[str, FeedHarvesterSourceItem] = {}


class MetadataConfig(UnhideBaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class IndexerConfig(BaseSettings):  # type: ignore
    """Pydantic settings class for the indexer configuration"""

    # we use settings to read from environment variables including secrets.
    model_config = SettingsConfigDict(env_file=('.env', '.env.dev', '.env.prod'), env_file_encoding='utf-8')
    base_solr_url: AnyUrl = Field(alias='SORL_URL', default=AnyUrl('http://solr:8983/solr/unhide'))
    data_dir: Path = Field(alias='DATA_DIR', default=Path('.').resolve())
    base_dir: Path = data_dir
    except_dir: Optional[Path] = None  # Field(default_factory=lambda: base_dir / 'exceptions')
    log_dir: Optional[Path] = None  # Field(default_factory=lambda: base_dir / 'logs'
    nthreads: int = 8
    solr_params: dict = {'commit': 'true'}
    ignore_keys: list = []
    entity_list: list = [
        'Person',
        'Organization',
        'Dataset',
        'CreativeWork',
        'SoftwareSourceCode',
        'SoftwareApplication',
        'Book',
        'Thesis',
        'Article',
        'DigitalDocument',
        'ScholarlyArticle',
        'Report',
        'Course',
        'ResearchProject',
        'DataCatalog',
        'Event',
    ]

    # @field_validator('base_dir')#, always=True)
    # @classmethod
    # def set_default_base_dir(cls, base_dir: Optional[Path], info: ValidationInfo) -> Path:
    #    if base_dir is None:
    #        base_dir = info.data['data_dir']
    #    return base_dir

    @field_validator('except_dir')
    @classmethod
    def set_default_except_dir(cls, except_dir: Optional[Path], info: ValidationInfo) -> Path:
        if except_dir is None:
            except_dir = info.data['data_dir'] / 'exceptions'
        return except_dir

    @field_validator('log_dir')
    @classmethod
    def set_default_log_dir(cls, log_dir: Optional[Path], info: ValidationInfo) -> Path:
        if log_dir is None:
            log_dir = info.data['data_dir'] / 'logs'
        return log_dir


class UploaderConfig(BaseSettings):  # type: ignore
    """Pydantic settings class for the indexer configuration"""

    # we use settings to read from environment variables including secrets.
    model_config = SettingsConfigDict(env_file=('.env', '.env.dev', '.env.prod'), env_file_encoding='utf-8')
    graph_name: str = Field(alias='DEFAULT_GRAPH', default='https://purls.helmholtz-metadaten.de/unhidekg')
    endpoint_url: AnyUrl = Field(alias='SPARQL_ENDPOINT', default=AnyUrl('http://localhost:8890/sparql'))
    username: str = Field(alias='DBA_USER', default='dba')
    passwd: SecretStr = Field(alias='DBA_PASSWORD', default=SecretStr('dba'))


class UnhideConfig(UnhideBaseModel):
    """Pydantic model for the unhide configuration file"""

    metadata: Optional[MetadataConfig] = None
    Aggregator: Optional[AggregatorConfig] = None
    GitHarvester: Optional[GitHarvesterConfig] = None
    SitemapHarvester: Optional[SitemapHarvesterConfig] = None
    OAIHarvester: Optional[OAIHarvesterConfig] = None
    DataciteHarvester: Optional[DataciteHarvesterConfig] = None
    IndicoHarvester: Optional[IndicoHarvesterConfig] = None
    FeedHarvester: Optional[FeedHarvesterConfig] = None
    Indexer: Optional[IndexerConfig] = None
    Uploader: Optional[UploaderConfig] = None
    DummyHarvester: Optional[DataciteHarvesterConfig] = None
