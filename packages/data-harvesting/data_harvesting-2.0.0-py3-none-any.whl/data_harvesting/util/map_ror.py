# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""This module contains functions to include metadata from ror.org for uplifting."""
import json
from io import BytesIO
import requests
import zipfile
from pathlib import Path
from typing import Dict, Any, cast, List
from data_harvesting.util.config import PKG_ROOT_DIR
# from typing_extensions import TypeAlias

# JSON: TypeAlias = Dict[str, "JSON"] | List["JSON"] | str | int | float | bool | None


ROR_DATA_PATH = PKG_ROOT_DIR.parent / 'external_data' / 'v1.46-2024-05-02-ror-data.json'
filename = str(ROR_DATA_PATH.stem) + '_schema_org' + '.json'
ROR_SCHEMA_DATA_PATH = PKG_ROOT_DIR.parent / 'external_data' / filename


# better have a function to update the ror data on demand, i.e pull the newses one from zenodo
# and put it into the folder
def download_ror_dump(
    source_url: str = 'https://zenodo.org/records/11106901/files/v1.46-2024-05-02-ror-data.zip?download=1', outpath: Path = ROR_DATA_PATH
):
    """Download and extract the latest ror data dump from zenodo"""
    # todo
    # get latest dump
    # set the two paths the latest version
    data_lines = None
    print(f'Downloading data file from source: {source_url}')
    req = requests.get(source_url, timeout=(10, 90))
    try:
        unzip = zipfile.ZipFile(BytesIO(req.content))
        unzip.extractall(outpath.parent)
    except zipfile.BadZipFile:
        print('Not a zip file or a corrupted zip file')

    if data_lines:
        with open(outpath, 'w') as stream:
            for line in data_lines:
                stream.write(line)


# This could also be done with a JQ mapping or something else. For now this is hardcoded.
# This seems also to be a common tasks, but I did not find a nice solution yet on the web.


def set_if_not_empty(datadict: dict, key: str, value):
    """Sets the key value in a given dictionary if the value is not None or empty"""
    if value is None:
        return datadict
    if value:  # not '',  [] .{}
        datadict[key] = value

    return datadict


def map_ror_schema_org(
    rordata: Dict[str, Any], schema_class: str = 'Organization', two_way_links: bool = False
):  # can also be ResearchOrganization
    """Takes json data provided by ror schema 2.0 and converts it into a standardized schema.org jsonld json.

    Example:

    {
        "id": "https://ror.org/01sf06y89",
        "name": "Macquarie University",
        "types": [
            "Education"
        ],
        "links": [
            "http://mq.edu.au/"
        ],
        "aliases": [],
        "acronyms": [],
        "status": "active",
        "wikipedia_url": "http://en.wikipedia.org/wiki/Macquarie_University",
        "labels": [],
        "email_address": null,
        "ip_addresses": [],
        "established": 1964,
        "country": {
            "country_code": "AU",
            "country_name": "Australia"
        },
        "relationships": [
            {
                "type": "Related",
                "label": "Sydney Hospital",
                "id": "https://ror.org/0402tt118"
            },
            {
                "type": "Child",
                "label": "ARC Centre of Excellence for Core to Crust Fluid Systems",
                "id": "https://ror.org/03nk9pp38"
            },
            {
                "type": "Child",
                "label": "ARC Centre of Excellence in Cognition and its Disorders",
                "id": "https://ror.org/044b7p696"
            },
            {
                "type": "Child",
                "label": "ARC Centre of Excellence in Synthetic Biology",
                "id": "https://ror.org/01p2zg436"
            }
        ],
        "addresses": [
            {
                "line": null,
                "lat": -33.775259,
                "lng": 151.112915,
                "postcode": null,
                "primary": false,
                "city": "Sydney",
                "state": "New South Wales",
                "state_code": "AU-NSW",
                "country_geonames_id": 2077456,
                "geonames_city": {
                    "id": 2147714,
                    "city": "Sydney",
                    "nuts_level1": {
                        "code": null,
                        "name": null
                    },
                    "nuts_level2": {
                        "code": null,
                        "name": null
                    },
                    "nuts_level3": {
                        "code": null,
                        "name": null
                    },
                    "geonames_admin1": {
                        "id": 2155400,
                        "name": "New South Wales",
                        "ascii_name": "New South Wales",
                        "code": "AU.02"
                    },
                    "geonames_admin2": {
                        "id": null,
                        "name": null,
                        "ascii_name": null,
                        "code": null
                    },
                    "license": {
                        "attribution": "Data from geonames.org under a CC-BY 3.0 license",
                        "license": "http://creativecommons.org/licenses/by/3.0/"
                    }
                }
            }
        ],
        "external_ids": {
            "ISNI": {
                "preferred": null,
                "all": [
                    "0000 0001 2158 5405"
                ]
            },
            "FundRef": {
                "preferred": null,
                "all": [
                    "501100001230"
                ]
            },
            "OrgRef": {
                "preferred": null,
                "all": [
                    "19735"
                ]
            },
            "Wikidata": {
                "preferred": null,
                "all": [
                    "Q741082"
                ]
            },
            "GRID": {
                "preferred": "grid.1004.5",
                "all": "grid.1004.5"
            }
        }

        ->

        {"context" : "http://schema.org",
        "@id": "https://ror.org/01sf06y89",
        "@type": "Organization",                        # "ResearchOrganization"
        "name": "Macquarie University",
        "types": [
            "Education"
        ],
        "url": [
            "http://mq.edu.au/"
        ], #if several same_as
        "aliases": [],
        "acronyms": [],
        "status": "active",
        "same_as": "http://en.wikipedia.org/wiki/Macquarie_University",
        "labels": [],
        "email_address": null,
        "ip_addresses": [],
        "foundingDate": 1964,
        "country": {
            "country_code": "AU",
            "country_name": "Australia"
        },
        "relationships": [
            {
                "type": "Related",
                "label": "Sydney Hospital",
                "id": "https://ror.org/0402tt118"
            },
            {
                "type": "Child",
                "label": "ARC Centre of Excellence for Core to Crust Fluid Systems",
                "id": "https://ror.org/03nk9pp38"
            },
            {
                "type": "Child",
                "label": "ARC Centre of Excellence in Cognition and its Disorders",
                "id": "https://ror.org/044b7p696"
            },
            {
                "type": "Child",
                "label": "ARC Centre of Excellence in Synthetic Biology",
                "id": "https://ror.org/01p2zg436"
            }
        ],
        "addresses": [
            {
                "line": null,
                "lat": -33.775259,
                "lng": 151.112915,
                "postcode": null,
                "primary": false,
                "city": "Sydney",
                "state": "New South Wales",
                "state_code": "AU-NSW",
                "country_geonames_id": 2077456,
                "geonames_city": {
                    "id": 2147714,
                    "city": "Sydney",
                    "nuts_level1": {
                        "code": null,
                        "name": null
                    },
                    "nuts_level2": {
                        "code": null,
                        "name": null
                    },
                    "nuts_level3": {
                        "code": null,
                        "name": null
                    },
                    "geonames_admin1": {
                        "id": 2155400,
                        "name": "New South Wales",
                        "ascii_name": "New South Wales",
                        "code": "AU.02"
                    },
                    "geonames_admin2": {
                        "id": null,
                        "name": null,
                        "ascii_name": null,
                        "code": null
                    },
                    "license": {
                        "attribution": "Data from geonames.org under a CC-BY 3.0 license",
                        "license": "http://creativecommons.org/licenses/by/3.0/"
                    }
                }
            }
        ],
        "external_ids": {
            "ISNI": {
                "preferred": null,
                "all": [
                    "0000 0001 2158 5405"
                ]
            },
            "FundRef": {
                "preferred": null,
                "all": [
                    "501100001230"
                ]
            },
            "OrgRef": {
                "preferred": null,
                "all": [
                    "19735"
                ]
            },
            "Wikidata": {
                "preferred": null,
                "all": [
                    "Q741082"
                ]
            },
            "GRID": {
                "preferred": "grid.1004.5",
                "all": "grid.1004.5"
            }
        }


    """

    def parse_relationships(rels: list, parse_parent: bool = two_way_links) -> dict:
        """parse the ror relationships of organizations

        parse_parent is per default false"""
        schema_rel: dict = {}
        for rel in rels:
            if rel['type'] == 'Child':
                sub_org = {'@id': rel['id'], '@type': 'Organization', 'name': rel['label']}
                sub_orgs = schema_rel.get('subOrganization', [])
                sub_orgs.append(sub_org)
                schema_rel['subOrganization'] = sub_orgs
            elif (rel['type'] == 'Parent') and parse_parent:
                par_org = {'@id': rel['id'], '@type': 'Organization', 'name': rel['label']}
                par_orgs = schema_rel.get('parentOrganization', [])
                par_orgs.append(par_org)
                schema_rel['parentOrganization'] = par_orgs
            else:  # Related
                pass  # we do not now how to map this, maybe into a 'related' field

        return schema_rel

    def parse_identifiers(ids: dict) -> list:
        """parse the external_ids field into https://schema.org/identifier"""
        schema_ids = []

        for key, val in ids.items():
            id_ = {'@type': 'PropertyValue', 'propertyID': key}  # can also be Text and URL
            value = val.get('all', None)
            if isinstance(value, list):
                if len(value) > 0:
                    value = value[0]
            id_['value'] = value
            schema_ids.append(id_)
        return schema_ids

    schema_org = {'@context': 'http://schema.org', '@type': schema_class}
    schema_org = set_if_not_empty(schema_org, '@id', rordata.get('id', None))
    schema_org = set_if_not_empty(schema_org, 'name', rordata.get('name', None))
    links = cast(List['str'], rordata.get('links', []))
    if len(links) > 0:
        schema_org = set_if_not_empty(schema_org, 'url', links[0])
    schema_org = set_if_not_empty(schema_org, 'foundingDate', rordata.get('established', None))
    # schema_org['address'] = None # rordata.get('addresses', None) # addresses

    rel = rordata.get('relationships', None)
    if rel is not None:
        schema_rel = parse_relationships(rel)
        schema_org = set_if_not_empty(schema_org, 'subOrganization', schema_rel.get('subOrganization', None))
        schema_org = set_if_not_empty(schema_org, 'parentOrganization', schema_rel.get('parentOrganization', None))
    schema_org = set_if_not_empty(schema_org, 'identifier', parse_identifiers(rordata.get('external_ids', {})))  # # external_ids, id
    schema_org = set_if_not_empty(schema_org, 'sameAs', rordata.get('wikipedia_url', None))  # external_ids
    org_types = cast(List['str'], rordata.get('types'))
    if 'Education' in org_types or 'Research' in org_types:
        schema_org['additionalType'] = 'ResearchOrganization'
    # schema_org['description'] = rordata.get('wikipedia_url', None)

    alternate_names = rordata.get('labels', []) + rordata.get('alias', []) + rordata.get('acronyms')
    # None # labels, alias, acronyms
    schema_org = set_if_not_empty(schema_org, 'alternateName', alternate_names)

    # clean Nones
    schema_org = rm_nones_dict(schema_org)

    return schema_org


def rm_nones_dict(datadict: dict, remove_empty_lists: bool = True) -> dict:
    """Recursively remove Nones and empty lists from nested dictionary"""
    final_dict: dict = {}
    for key, val in datadict.items():
        if not val:
            continue
        if isinstance(val, dict):
            new = rm_nones_dict(val)  # ! recursion
            if len(new.keys()) > 0:
                final_dict[key] = new

        elif isinstance(val, list):
            new_list = []
            for item in val:
                if isinstance(item, dict):
                    new = rm_nones_dict(item)  # ! recursion
                    if len(new.keys()) > 0:
                        new_list.append(new)
                elif item is not None:
                    new_list.append(item)
            if remove_empty_lists:
                if len(new_list) > 0:
                    final_dict[key] = new_list
            else:
                final_dict[key] = new_list
        else:
            final_dict[key] = val

    return final_dict


def map_all_ror_to_schema_org(ror_data: Path = ROR_DATA_PATH, output: Path = ROR_SCHEMA_DATA_PATH) -> None:
    """
    Map the whole ror dump to schema.org once and store it. this is faster as, if we convert each
    institution x times during indexing.

    Or convert on the fly, and entries which exists are not indexed and converted again...
    but this will also mean that the indexing might fail, due to the conversion.

    Either way this function is still useful for testing.
    """
    if not ror_data.exists():
        print('Ror dump not present. I try to download ror data.')
        download_ror_dump()

    with open(ror_data, 'r', encoding='utf-8') as stream:
        data = json.load(stream)

    schema_org_ror = {}  # should be of the form {identifier : data}

    for i, entry in enumerate(data):
        print(i)
        # print(entry)
        mapped = map_ror_schema_org(entry)
        id_ = mapped.get('@id')
        schema_org_ror[id_] = mapped

    print(f'Parsed {len(list(schema_org_ror.keys()))} entries')
    with open(output, 'w', encoding='utf-8') as stream:
        json.dump(schema_org_ror, stream, sort_keys=True, indent=2, separators=(',', ': '))


def get_ror_schemadata_by_id(ror_id: str, ror_data_file: Path = ROR_SCHEMA_DATA_PATH):
    """
    From the given ror dump file (or database storage location) get the ror metadata dict for
    a given ror identifier.
    """
    if not ror_data_file.exists():
        raise FileExistsError(f'The provided path {ror_data_file}, does not exists')

    with open(ror_data_file, 'r', encoding='utf-8') as stream:
        data = json.load(stream)

    org_ror = data.get(ror_id, None)
    return org_ror


# This was implemented in a different repository for trails. I leave it here as a reference.
# def request_match_ror_api(affiliation_str):
#    """
#    Find out
#    example
#    curl "https://api.ror.org/organizations?affiliation=Peter+Gruenberg+Institute+Froschungszentrum+Juelich"
#    We played around with this. fuzzy and the other matching is not good enough
#    """
#    pass
