# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""This module contains functions to wrap and enhance rdflib."""
from __future__ import annotations

from .config import PKG_ROOT_DIR
from typing import Literal, Optional, Union, Any
from pathlib import Path
import rdflib
import wrapt
import vcr

# using default in-memory rdflib triple store
DEF_RDF_STORE = None

# alternative backend store provided via oxrdflib,
# but it seems to have still enough bugs with serialization and parsing
# to better stay away from it for now.
# DEF_RDF_STORE = "Oxigraph"
#
# could also try Virtuoso store: https://pythonhosted.org/virtuoso/rdflib.html

# global caching setting
# DEF_CACHE_PATH = None  # cache disabled
DEF_CACHE_PATH = PKG_ROOT_DIR / 'external_schema' / 'context_cache.yaml'


# global cache behavior mode
CacheMode = Literal['r', 'w', 'a']
# DEF_CACHE_MODE = 'w'  # create new cache from scratch
# DEF_CACHE_MODE = 'a'  # create / update existing
DEF_CACHE_MODE: CacheMode = 'r'  # use cache


class CachingGraph(wrapt.ObjectProxy):  # type: ignore
    """Wrapper for rdflib graph to modularize storage backend and control internet access.

    Is used to intercept and collect network responses, block network access and deliver cached or mock responses.

    NOTE:
        This has not been tested with parallelization!  It _might_ work for read-only use of the cache,
        but it most likely _will_ fail for parallel recording, because it uses a normal YAML file for the cassette!
    """

    def __init__(self, store: Optional[Any] = None, cache_mode: CacheMode = DEF_CACHE_MODE, cache_path: Optional[Path] = None, **kwargs):
        """Create a new rdflib Graph (wrapped by caching functionality for parse method).

        Args:
            storage: Some valid rdflib Graph storage backend
            cache_path: Path to cache file for network requests (if not set, cache is not used)
            cache_mode: 'r' - will use existing cache, 'a' - use + update, 'w' - create and record fresh cache

        """
        use_store = store or DEF_RDF_STORE
        if use_store is not None:
            kwargs['store'] = use_store  # can't pass None to Graph constructor
        super().__init__(rdflib.Graph(**kwargs))

        self._cache_mode = dict(a='new_episodes', r='none', w='all')[cache_mode]
        self._cache_path = cache_path or DEF_CACHE_PATH

    def parse(self, *args, **kwargs) -> CachingGraph:
        if not self._cache_path:
            self.__wrapped__.parse(*args, **kwargs)
        else:
            with vcr.use_cassette(self._cache_path, record_mode=self._cache_mode, allow_playback_repeats=True):
                self.__wrapped__.parse(*args, **kwargs)
        return self

    def __contains__(self, key):
        return key in self.__wrapped__


def is_graph(obj):
    return isinstance(obj, (rdflib.Graph, CachingGraph))


def copy_graph(obj: Union[rdflib.Graph, CachingGraph], **kwargs):
    return type(obj)(**kwargs).parse(data=obj.serialize())


Graph = CachingGraph
