# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
Module containing the Aggregator class, which performs uplifting and data
enrichments on the data represented as a  data-harvesting LinkedDataObject class.
"""

from importlib_metadata import EntryPoint
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, cast


from data_harvesting import get_config, get_config_path
from data_harvesting.data_model import LinkedDataObject
from data_harvesting.util.config import PKG_ROOT_DIR
from data_harvesting.model_core import AggregatorConfig, AggregatorStackItem
from data_harvesting.util.sparql_util import apply_update, get_update_from_file
from data_harvesting.util.rdf_util import Graph, is_graph
from data_harvesting.rdfpatch import RDFPatch


# We clearly separate aggregation function from the data object. Since data
# itself should not change
class Aggregator:
    """
    Class to aggregate LinkedDataObjects, or databases by predefined sparql updates
    within a given config file, and or in addition to given operations.
    All operations together form the stack to apply by the Aggregator.

    The form of stack items is defined by the AggregatorStackItem pydantic model

    Comments:
    # Add prov-o terms to data.

    :param stack: A stack to initialize the Aggregator with
    :type stack: List[AggregatorStackItem](,optional)
    :param config_path:
    :type config_path: pathlib.Path(, optional)
    """

    # read from config file which operations to apply
    #
    def __init__(self, stack: Optional[List[AggregatorStackItem]] = None, config_path: Optional[Path] = None):
        """Constructor method for an Aggregator instance and read a task stack from a given config file.

        :param stack: A stack to initialize the Aggregator with
        :type stack: List[AggregatorStackItem](,optional)
        :param config_path:
        :type config_path: pathlib.Path(, optional)
        """
        stack = stack or []
        config_path = config_path or get_config_path()

        self.config = AggregatorConfig()
        if config_path is not None:
            self.set_config(config_path=config_path)

        # the aggregator uses aggretator functions from config (if given), and then the ad-hoc passed ones
        self.stack = self.config.stack + stack

    def set_config(self, config_path: Optional[Path] = None) -> None:
        """Set sources and harvester specific configurations from a given config.

        :param config_path: The path to the configuration file to use, defaults the default config
        :type config_path: pathlib.Path(, optional)
        """

        config_path = config_path or get_config_path()
        full_config = get_config(config_path)
        # parse the aggregator-specific part in the config
        self.config = AggregatorConfig.model_validate(full_config.get(self.__class__.__name__, {}))

    def to_string(self) -> str:
        """Display the stack as a string. This comes handy for serialization."""
        return str(self.stack)

    def add_to_stack(self, *items) -> None:
        """Add a task to the stack."""
        self.stack += items

    def apply_to(self, data_object: LinkedDataObject) -> LinkedDataObject:
        """Apply the given stack to the given data_object in line.
        The changes are applied to the derived data and then the patch_stack is updated.

        :param data_object: The LinkedDatObject to apply the tasks in the stack to
        :type data_object: data_harvesting.LinkedDataObject
        :raises ValueError: Aggregator command in stack not understood, unknown type in
        :return: A new LinkedDataObject with the uplifted data
        :rtype: data_harvesting.LinkedDataObject
        """
        patch_stack = data_object.patch_stack
        derived = data_object.derived  # an Union(dict, list
        if isinstance(derived, dict):
            context = derived.get('@context', {})  # we assume here that the context does not change
        else:
            for entry in derived:
                context = entry.get('@context', None)
                if context:  # fornow just use the first one found...
                    break

        # a feature which changes prefixes needs to change also this.
        for item in self.stack:
            # store prov on this small level or higher level, i.e on patch versus many
            patch: Optional[RDFPatch] = None

            if item.type == 'python':
                method = EntryPoint(name=None, group=None, value=item.method).load()
                # TODO make this more robust, i.e the methods needs to have a patch decorator...
                # but for functions taking the dict, there is no graph input
                # TODO how to do patches for these?
                # be careful derived can now be a graph
                previous = derived
                derived = method(data=previous, *item.args_, **item.kwargs_)

            elif item.type == 'sparql':
                basepath = PKG_ROOT_DIR / 'data_enrichment'  # TODO get from config if set
                assert item.file is not None
                filepath = basepath / item.file
                update = get_update_from_file(filepath)
                # sparql functions always need a graph
                if not is_graph(derived):
                    derived = Graph().parse(data=json.dumps(derived), format='json-ld')

                patch, derived = apply_update(graph=derived, sparql_update=update)

                patch.metadata.sparql_update_path = item.file  # type: ignore
                # patch.metadata['sparql_update'] = update

            else:
                raise ValueError(f'Aggregator command in stack not understood, unknown type in: {item}.')

            if patch is not None:  # TODO only add patch if the patch is not empty...
                if patch.add_triples or patch.delete_triples:
                    patch_stack.append(patch)

        data_object.patch_stack = patch_stack
        if isinstance(derived, dict):
            pass
        elif is_graph(derived):
            g = cast(Graph, derived)
            derived = json.loads(g.serialize(format='json-ld', encoding='utf-8', context=context, sort_keys=False))
            # this serialzation can differ each time...
            # the returned is in the form of the json-ld graph notation, which nice, but not so human readable
            # derived = jsonld.compact(derived)
        data_object.derived = derived
        data_object.metadata.last_modified_at = datetime.now()

        return data_object
