# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
Module containing the RDFPatch class, as well as some methods around it, which are useful to
generate and work with patches for rdf data.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, cast, Optional, Union
from typing_extensions import Annotated

from pydantic import Field
from pydantic.functional_serializers import PlainSerializer
from pydantic.functional_validators import PlainValidator
from rdflib.compare import graph_diff
from rdflib import Graph

from data_harvesting.model_core import UnhideBaseModel, ProcessMetadata
from data_harvesting.util.rdf_util import CachingGraph, is_graph, copy_graph


# This is used as type hint to define a pydantic field for rdfgraphs:


def to_rdfgraph(obj: Union[Graph, str]) -> Graph:
    """Load an rdflib graph from a given ttl string"""
    if is_graph(obj):
        return obj

    graph = CachingGraph()
    if obj.strip():
        graph.parse(data=obj)  # be more careful here, much can go wrong ;-)
    return graph


def from_rdfgraph(graph: Union[Graph, str]) -> str:
    """Serializer for an rdflib graph returns and serialized graph as a ttl string"""
    # not sure if the string is ever needed
    if is_graph(graph):
        ret = cast(Graph, graph).serialize(format='ttl')
    else:
        ret = graph
    return cast(str, ret)


RdflibGraphType = Annotated[
    Graph,
    PlainValidator(to_rdfgraph),
    PlainSerializer(from_rdfgraph),
    Field(default_factory=Graph),
]

# ----


class RDFPatchMetadata(ProcessMetadata):
    """Extended provenance-tracking metadata for RDF patches."""

    function_module: str = '?'
    function_name: str = '?'

    sparql_update_path: Optional[Path] = None


class RDFPatch(UnhideBaseModel):
    """
    This class represents a RDF patch

    Created, since one could not parse the Jena Patch format into a simple RDF graph and
    rdf-delta is in java (https://github.com/afs/rdf-delta).

    If there is a other common way already out there this should be used instead
    for example see: https://www.w3.org/TR/ldpatch/

    and https://github.com/pchampin/ld-patch-py (LGPL).
    There are other formats one could serialize a patch to. These do not overlap in power.
    Problems with the current implementation of this:
    - Merging of a stack of RDFPatches would not work properly by the current 'several graph' design,
    since the order of the transactions matters...
    """

    add_triples: RdflibGraphType
    delete_triples: RdflibGraphType
    metadata: RDFPatchMetadata = Field(default_factory=RDFPatchMetadata)

    def serialize(self, destination: Path):
        """
        Serialize the file to a json document, while the graph data is stored in a specific format
        """
        total_json = self.model_dump_json()
        with open(destination, 'w', encoding='utf-8') as fileo:
            fileo.write(total_json)

    @classmethod
    def from_filename(cls, filename: Path) -> RDFPatch:
        """Initialize/Load LinkedDataObject from filename"""
        if not filename.is_file():
            raise ValueError(f'Source file path provided: {filename} is not a file, or does not exist.')
        with open(filename, 'r', encoding='utf-8') as fileo:
            data = fileo.read()
        instance = cls.model_validate_json(data)
        return instance

    @classmethod
    def from_graph_diff(cls, in_first: Graph, in_second: Graph, *, metadata: Optional[RDFPatchMetadata] = None) -> RDFPatch:
        """
        Generate a rdf patch for a given graph difference

        :param in_first: a graph, set of triples containing triples only in the first/input graph from a diff, i.e. these were deleted
        :type in_first: Graph
        :param in_first: a graph, set of triples containing triples only in the second/output graphfrom a diff, i.e. these were added
        :type in_first: Graph

        In the first implementation this returned an RDFpatch in the Jena format
        see: https://jena.apache.org/documentation/rdf-patch/, or https://github.com/afs/rdf-delta
        now its a list of triples in ttl format until there is wwwc consensus on
        the rdfpatch format.
        """
        ret = RDFPatch(add_triples=in_second, delete_triples=in_first)
        ret.metadata = metadata or ret.metadata
        return ret

    def apply(self, graph: Graph) -> Graph:
        """
        Apply this patch to a graph
        Since a patch is written a specific backend triple store like jena, this provides a way to apply
        the patch through python to a given graph outside of the backened
        """
        # todo implement PA
        # EX = Namesspace('')
        # o_graph.bind()
        o_graph = graph + self.add_triples - self.delete_triples
        return o_graph

    def revert(self, graph: Graph) -> Graph:
        """
        Revert this patch from a graph
        Since a patch is written a specific backend triple store like jena, this provides a way to apply
        the patch through python to a given graph outside of the backened
        """
        # todo implement PA
        o_graph = graph - self.add_triples + self.delete_triples
        return o_graph


# What about patch sequences? then the current class is not sufficient. since graph, can not captures
# order

# Decorator to mark functions processing RDF graphs


def generate_patch(graph_key='graph') -> Callable:
    """
    Generate a rdf patch for a given function which inputs a graph and outputs a graph.
    This function is meant to be used as a decorator generator.

    In order to find the graphs the input graph has to be the first argument to the function func,
    or a kwarg with the key provided by graph_key, default 'graph'.
    Also to find the output graph it requires the return value or the first return value to be a graph

    returns function
    raises ValueError
    """

    def generate_patch_decorator(func, graph_key='graph'):
        """
        The actual decorator
        """

        def _generate_patch(*args, **kwargs):
            """
            returns the results of func plus a patch in front
            """
            # copy because graph is parsed per reference, often this will lead then to
            # the output graph == input graph after function execution
            if graph_key in kwargs:
                graph = copy_graph(kwargs[graph_key])
            else:
                if len(args) > 0:
                    if is_graph(args[0]):
                        graph = copy_graph(args[0])
                    else:
                        raise ValueError(f'No input graph found! Has to be provided first argument, or a kwargs {graph_key}!')

            results = func(*args, **kwargs)

            out_graph = None
            if is_graph(results):
                out_graph = results
            elif isinstance(results, list):
                if len(results) > 0:
                    if is_graph(results[0]):
                        out_graph = results[0]
            if out_graph is None:
                raise ValueError('No output graph found! Has to single return or first return!')

            in_both, in_first, in_second = graph_diff(graph, out_graph)

            # this might be error prone, try except or else?
            # serializable_args = (str(arg) for arg in args)
            # serializable_kwargs = {key: str(val) for key, val in kwargs.items()}

            metadata = RDFPatchMetadata(function_module=func.__module__, function_name=func.__name__)

            # It would be nice to store more metadata on the input, but currently I do not know how
            # to make sure that the patch stays serializable. i.e everything simple data types.
            # very often we have Graphs, which causes a problem wit pydantic
            #'function_args': serializable_args,
            #'function_kwargs': serializable_kwargs,

            patch = RDFPatch.from_graph_diff(in_first, in_second, metadata=metadata)

            return patch, results

        return _generate_patch

    return generate_patch_decorator
