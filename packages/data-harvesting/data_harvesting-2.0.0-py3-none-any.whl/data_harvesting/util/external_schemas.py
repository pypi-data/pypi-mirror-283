# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
Utility to download, load and process external schemas needed for example validation
"""

from pathlib import Path

import requests

from data_harvesting.util.rdf_util import Graph

EXTERNAL_SCHEMAS_FOLDER = Path(__file__).resolve().parent.parent / 'external_schema'
KNOWN_SCHEMAS = {
    'schema_org': 'https://schema.org/version/latest/schemaorg-current-https.jsonld',
    'schema_org_shacl': 'https://datashapes.org/schema.jsonld',
    'codemeta': 'https://doi.org/10.5063/schema/codemeta-2.0',
}


def cached_schema_path(schema_name: str) -> Path:
    return EXTERNAL_SCHEMAS_FOLDER / f'{schema_name}.jsonld'


def load_external_schema(schema_name: str = 'schema_org_shacl') -> Graph:
    """
    Read a schema from file if it is there, otherwise download it and cache in a file.
    """

    if schema_name not in KNOWN_SCHEMAS:
        raise ValueError(f'Schema: {schema_name} not known. Could not be loaded.')

    schema_path = cached_schema_path(schema_name)
    if not schema_path.exists():
        data = requests.get(KNOWN_SCHEMAS[schema_name], timeout=(10, 100)).text  # content
        with open(schema_path, 'w', encoding='utf-8') as fileo:
            fileo.write(data)

    schema = Graph().parse(schema_path)

    return schema
