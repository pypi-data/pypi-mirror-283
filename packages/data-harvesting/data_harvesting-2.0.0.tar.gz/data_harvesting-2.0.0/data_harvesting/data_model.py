# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
Module containing the Data model for linked data close to the unhide projects needs,
which wraps the original data stored metadata and provenance data
together with derived data for the actual graph.
"""
from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
from typing import Annotated, List, Optional, Union

from importlib.metadata import version
from pydantic import Field
from pyshacl import validate as shacl_validate

from data_harvesting.model_core import UnhideBaseModel, ProcessMetadata
from data_harvesting.rdfpatch import RDFPatch
from data_harvesting.util.external_schemas import load_external_schema
from data_harvesting.util.rdf_util import Graph
from data_harvesting.util.url_util import make_url_save

SCHEMA_ORG_SHAPE = load_external_schema('schema_org_shacl')

THIS_PKG_VERSION = version('data-harvesting')


class LDOMetadata(ProcessMetadata):
    """Administrative/technical metadata attached to objects by unhide processes."""

    last_modified_at: datetime = Field(default_factory=lambda: datetime.now().isoformat())  # type: ignore
    data_harvesting_version: str = THIS_PKG_VERSION


class LinkedDataObject(UnhideBaseModel):
    """
    Representation of a json-ld file with Original data, derived data, and metadata including provenance

    This is a pydantic data models with different constructor methods as well as
    support for shacl validation beyond what pydantic does

     ..code-block::

       {
       metadata: {},
       original: {},
       derived: {},
       patch_stack: []
       }

    Each LinkedDataObject usually has a representative file on disk or data object in an object store
    The derived (uplifted) data can be put it into the a combined graph (like the Helmholtz knowledge graph).

    # Comments:
    # Provenance might/should be tract somewhere externally, like through a workflow manager (AiiDA)
    # One might also use this or write a base class which can abstract from the actual storage,
    # like if it is stored on disk, or in an objectstore or some other database
    # Apply filter prior serialization, to allow for removal of certain internal data
    """

    metadata: Annotated[LDOMetadata, Field(default_factory=LDOMetadata)]
    original: Union[List[dict], dict]
    derived: Annotated[Union[List[dict], dict], Field(default_factory=lambda: [])]
    patch_stack: Annotated[List[RDFPatch], Field(default_factory=lambda: [])]

    def __init__(self, **data):
        """Constructor methods"""
        super().__init__(**data)
        if not self.derived:
            if len(self.patch_stack) == 0:
                self.derived = self.original

    def serialize(self, destination: Path):
        """
        Serialize the LinkedDataObject to a json document, while the graph data is stored in a specific format

        :param destination: The Path to serialize to object to
        :type destination: Path
        """
        total_json = self.model_dump_json()
        dct = json.loads(total_json)  # to JSONify types
        with open(destination, 'w', encoding='utf-8') as fileo:
            # for custom formatting re-dump
            json.dump(dct, fileo, indent=4, separators=(', ', ': '), sort_keys=True)

    @classmethod
    def from_filename(cls, filename: Path):
        """Initialize/Load LinkedDataObject from filename

        :param filename: The Path to load from
        :type filename: Path
        :raises ValueError: If filename does not exists or is not a file.
        """
        if not filename.is_file():
            raise ValueError(f'Source file path provided: {filename} is not a file, or does not exist.')
        # with open(filename, 'r', encoding='utf-8') as fileo:
        #    data = fileo.read() # why not json load
        with open(filename, 'r', encoding='utf-8') as fileo:
            data = json.load(fileo)
        # instance = cls.model_validate_json(data)

        instance = cls.from_dict(data)
        return instance

    @classmethod
    def from_dict(cls, data: dict):
        """Initialize/Load LinkedDataObject from a given dict

        :param data: The json dictionary to initialize an LinkedData object from
        :type data: dict
        """
        safe_data = make_url_save(data)
        instance = cls.model_validate(safe_data)
        return instance

    def validate_rdf(
        self,
        shape_graph: Optional[Graph] = None,
        original_only: bool = False,
        verbose: bool = False,
    ):
        """Do a shacl validation on the original data and derived versus a given shape graph

        todo get the default shape graph
        =SCHEMA_ORG_SHAPE

        :param shape_graph: The shape graph to validate against, defaults to schema.org shape graph
        :type shape_graph: rdflib.Graph(,optional)
        :param original_only: Validate only the original data and not the derived part?
        :type original_only: bool
        :param verbose: More verbose output?
        :type verbose: bool
        """
        shape_graph = shape_graph or SCHEMA_ORG_SHAPE
        orgi_graph = Graph()
        orgi_graph.parse(data=json.dumps(self.original), format='json-ld')
        val_org = shacl_validate(orgi_graph, shacl_graph=shape_graph)
        conforms, results_graph, results_text = val_org

        if verbose:
            print(results_text)

        if not original_only:
            de_graph = Graph()
            de_graph.parse(data=json.dumps(self.derived), format='json-ld')
            val = shacl_validate(de_graph, shacl_graph=shape_graph)
            conforms_de, results_graph, results_text = val
            conforms = conforms and conforms_de

        if verbose:
            print(results_text)

        return conforms
