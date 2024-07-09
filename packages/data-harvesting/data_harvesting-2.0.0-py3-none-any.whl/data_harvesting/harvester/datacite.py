# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
This module contains util and a class to harvest metadata from data cite with respect to organizations

given a ROR identifier a query is posted to the graphql API of datacite to receive all
connected PIDS. Then over an API request the full datacite metadata is extracted for each of these PIDS
This metadata is then converted to a desired format.
"""

import binascii
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

import progressbar
import requests

from data_harvesting.data_model import LinkedDataObject
from data_harvesting.harvester.base import BaseHarvester, HarvesterMetadata

logger = logging.getLogger('data_harvesting')


def convert_datacite(metadata: dict, dataformat: str = 'schema.org jsonld'):
    """
    Convert a given datecite metadata entry to some other format default schema.org json-ld

    :param metadata: [description]
    :type metadata: [type]
    :param dataformat: [description], defaults to schema.org jsonld
    :type dataformat: str, optional
    """
    pass
    # under the xml key is the whole metadata in Base64


def correct_keywords(mdata: dict) -> dict:
    """Data cite provides all keywords in a single string, also it adds topic to keywords

    The frontend expects here a list.
    # TODO maybe add something to deal with the field syntax > >.
    # TODO: maybe also make this a set of keywords to avoid duplicates
    # TODO: enrich keywords via AI extractions from title and abstract texts and also how these
    # correspond to a certain field.
    # TODO: generalize, if a list of dicts is given, or keywords are nested further down
    """
    keywords = mdata.get('keywords', None)
    new_data = mdata.copy()  # do not do inline changes
    if (keywords is not None) and isinstance(keywords, str):
        keywords = keywords.split(',')
        keywords = [keyword.strip() for keyword in keywords]

        new_data['keywords'] = keywords
    return new_data


def extract_metadata_restapi(pid: str) -> Optional[dict]:  # etree
    """
    Request the datacite metadata for a given pid over the rest API
    """
    # parse doi to right format 10.5438/0012
    doi = pid.lstrip('https://doi.org/')
    base_url = 'https://api.datacite.org/dois/'
    record_url = base_url + doi
    # application/ld+json text/turtle
    # Does datacite always deliver schema.org here? this might change in the future
    headers = {'Accept': 'application/ld+json'}
    req = requests.get(record_url, headers=headers, timeout=(10, 60))

    if req.status_code == 200:
        datacite_json: Optional[dict] = req.json()
        if datacite_json is None:
            time.sleep(0.02)  # Otherwise this sometimes is None, and gets later filled, i dont know why
            # maybe because of the 'Accept': 'application/ld+json'
    else:  # req.status_code !=200
        datacite_json = None
    return datacite_json


def query_graphql_api(
    ror: str,
    max_count: int = 2000,
    get_all: bool = True,
    since: Optional[datetime] = None,
) -> Tuple[List[str], List[List[dict]]]:
    """
    Query the Graphql graph of Datacite over the API

    We do this instead of a query to the normal API, because the graph contains more aggregated links
    to works. Through the PIDS of works in the Graph do not have to correspond to the PIDS of the same
    work in the usual Datacite API.


    example:
    curl 'https://api.datacite.org/graphql' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json'
    -H 'Accept: application/json' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://api.datacite.org' --data-binary '{"query":"{organization(id: \"https://ror.org/02nv7yv05\") {\nid name\n    works (first:3){nodes {id}}}}"}' --compressed

    # The api is a bit unstable, or restricted, this is why serialize the data
    #todo implement since, i.e the 'updated' key
    # one way is published:"2022"
    # get year of publication
    """
    url = 'https://api.datacite.org/graphql'
    query = """query {organization(id: "https://ror.org/02nv7yv05") {
id name alternateName wikipediaUrl citationCount viewCount
    downloadCount
    works (first:3){totalCount
      published {
        title count}
      resourceTypes {
        title count}
      nodes {id}}}}"""
    # query = '{organization(id: \"https://ror.org/02nv7yv05\") {id name works (first:'+ str(max_count) + '){totalCount nodes {id}}}}'
    query = (
        '{organization(id: '
        + f'"{ror}"'
        + ') {id name works (first:'
        + str(max_count)
        + '){totalCount pageInfo {endCursor hasNextPage} nodes {id doi publisher{name publisherIdentifier} relatedIdentifiers{relatedIdentifier relationType}}}}}'
    )
    if since is not None:
        year = since.year  # This means we will only pick up the next year after the harvester ran a second time.
        query = (
            '{organization(id: '
            + f'"{ror}"'
            + ') {id name works (first:'
            + str(max_count)
            + f' published:"{year}"'
            + '){totalCount pageInfo {endCursor hasNextPage} nodes {id doi publisher{name publisherIdentifier} relatedIdentifiers{relatedIdentifier relationType}}}}}'
        )
    logger.info(f'graphql query: {query}')
    query_f = query  # .format(ror, max_count)#=ror, max_count=max_count)
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://api.datacite.org',
    }
    req = requests.post(url, json={'query': query_f}, headers=headers, timeout=(10, 600))

    if req.status_code == 200:
        json_data: Optional[dict] = req.json()
        if json_data is None:
            time.sleep(0.02)
    else:
        logger.error(f'Failed to query datacite graphql API for {ror}')
        return [], []

    if json_data is None:
        logger.error(f'No data found for {ror}')
        return [], []

    # print(json_data)
    json_data_all = json_data
    total_count = json_data['data']['organization']['works']['totalCount']
    logger.info(f'Found {total_count} records for {ror}')
    pid_list = [val['id'] for val in json_data['data']['organization']['works']['nodes']]
    if (total_count >= max_count) and get_all:
        # we missed some records, query again to get all
        further_queries = total_count // max_count
        for i in range(further_queries):
            last_id = json_data['data']['organization']['works']['pageInfo']['endCursor']  # type: ignore
            # offset is not supported by datacite graphql api, but after is
            query_f = (
                '{organization(id: '
                + f'"{ror}"'
                + ') {id name works (first:'
                + str(max_count)
                + ' after: "'
                + last_id
                + '"){totalCount pageInfo {endCursor hasNextPage} nodes {id doi publisher{name publisherIdentifier} relatedIdentifiers{relatedIdentifier relationType}}}}}'
            )
            logger.info(f'Query to graphql: {query_f}')
            req = requests.post(
                url, json={'query': query_f}, headers=headers, timeout=(10, 600)
            )  # query.format(ror=ror, max_count=max_count)})
            json_data = json.loads(req.text)
            pid_list.extend([val['id'] for val in json_data['data']['organization']['works']['nodes']])  # type: ignore
            nodes_all = json_data_all['data']['organization']['works']['nodes']
            nodes_all.extend(json_data['data']['organization']['works']['nodes'])  # type: ignore
            json_data_all['data']['organization']['works']['nodes'] = nodes_all

    return pid_list, json_data_all  # type: ignore


def harvest_ror(
    ror: str,
    since: Optional[datetime] = None,
    base_savepath: Optional[Path] = None,
    skip_existing: Optional[bool] = True,
    use_cached_ql: Optional[bool] = True,
    unhidedata: bool = True,
):  # pylint: disable=too-many-statements
    """
    For each pid related to the ror identifier, down load all metadata records

    updated since then.
    """
    failed_records: List[str] = []
    successful_records: List[str] = []
    file_links: List[Path] = []

    if base_savepath is None:
        base_savepath = Path('.') / 'datacite'

    base_savepath.mkdir(parents=True, exist_ok=True)

    if ror.endswith('/'):
        ror.strip('/')
    ror_end = ror.split('/')[-1]

    today = datetime.today().isoformat().split('T')[0]

    base_temp = base_savepath.parent / 'temp'
    base_temp.mkdir(parents=True, exist_ok=True)

    graph_query: Path = base_temp / f'graph_ql_res_{ror_end}_{today}.json'

    pid_list_path: Path = base_temp / f'pid_list_{ror_end}_{today}.txt'
    store = True

    if pid_list_path.exists() and graph_query.exists() and use_cached_ql:
        store = False
        with open(graph_query, 'r', encoding='utf-8') as fileo:
            json_data = json.load(fileo)
        with open(pid_list_path, 'r', encoding='utf-8') as fileo:
            record_pids = fileo.readlines()
    else:
        record_pids, json_data = query_graphql_api(ror, since=since)

    if len(record_pids) == 0:
        return [], [], []

    if store:
        with open(graph_query, 'w', encoding='utf-8') as fileo:
            json.dump(json_data, fileo, indent=4, separators=(', ', ': '), sort_keys=True)
        with open(pid_list_path, 'w', encoding='utf-8') as fileo:
            for item in record_pids:
                fileo.write(f'{item}\n')

    logger.info(f'Harvesting {len(record_pids)} record pids from Datacite {ror}')
    with progressbar.ProgressBar(max_value=len(record_pids)) as pbar:
        for i, record in enumerate(record_pids):
            pbar.update(i)
            if unhidedata:
                filename = binascii.hexlify(record.encode('utf-8')).decode() + '.json'
            else:
                filename = binascii.hexlify(record.encode('utf-8')).decode() + '.jsonld'
            jsonld_filepath: Path = base_savepath / filename
            if jsonld_filepath.exists() and skip_existing:
                successful_records.append(record)
                file_links.append(jsonld_filepath)
                continue
            mdata = extract_metadata_restapi(record)

            if mdata is None:
                # look into related identifiers sameAs is in Datacite IsVariantFormOF
                related_identifier = json_data['data']['organization']['works']['nodes'][i]['relatedIdentifiers']
                for identifier in related_identifier:
                    if identifier['relationType'] == 'IsVariantFormOf':
                        # Maybe this should be in bulk or over OAI-PMH
                        mdata = extract_metadata_restapi(identifier['relatedIdentifier'])
                if mdata is None:
                    logger.warning(f'Failed, to retrieve jsonld {record}')
                    failed_records.append(record)
                    continue
            mdata = correct_keywords(mdata)  # TODO: since we change the original data here: we might
            # want to move this into some uplifting tasks (also if for other sources) and track the
            # provenance for it.
            modified = mdata.get('updated', None)
            if modified is not None:
                modified = datetime.fromisoformat(modified)
                print(f'here: {modified}')
                if modified > since:
                    continue  # skip
            if unhidedata:  # store as linked data.
                metadata = HarvesterMetadata(
                    harvester_class='DataciteHarvester', source_pid=record, provider='Datacite', preprocess='prov:corrected_keywords'
                )
                ldo = LinkedDataObject(original=mdata, derived=mdata, patch_stack=[], metadata=metadata)
                ldo.serialize(destination=jsonld_filepath)
            else:  # just dump what was found
                with open(jsonld_filepath, 'w', encoding='utf-8') as fileo:
                    json.dump(mdata, fileo, indent=4, separators=(', ', ': '), sort_keys=True)
            successful_records.append(record)
            file_links.append(jsonld_filepath)

    return successful_records, file_links, failed_records


class DataciteHarvester(BaseHarvester):
    """This is the Harvester to crawl sitemap.xmls and extract metadata from resulting urls.

    the Urls can be selected according to a given pattern.
    the main target metadata is json-LD which is schema.org conform
    """

    def run(
        self,
        source='all',
        since: Optional[datetime] = None,
        base_savepath: Optional[Path] = None,
        **kwargs,
    ):
        """Execute the harvester for a given center or all"""
        since = since or self.get_last_run(source)
        base_savepath = base_savepath or self.outpath

        fails = []
        links = []
        sucs = []
        logger.info(f'Dataciteharvester last run: {since}')
        rors = {key: val for key, val in self.get_sources().items() if source in (key, 'all')}

        for key, val in rors.items():
            logger.info(f'Harvesting Center {key}')
            ror = val['ror']
            base_savepath1 = base_savepath / key
            suc, links, fail = harvest_ror(ror, base_savepath=base_savepath1, since=since)
            fails.extend(fail)
            sucs.extend(suc)

        logger.info(f'Successfully harvested {len(sucs)} records.')
        logger.info(f'Failed to harvest {len(fails)} records')

        self.append_last_harvest(links)
        self.append_failures(fail)
        self.append_successes(suc)
        self.set_last_run(source)
        self.dump_last_harvest(source=source)  # control destination here.
