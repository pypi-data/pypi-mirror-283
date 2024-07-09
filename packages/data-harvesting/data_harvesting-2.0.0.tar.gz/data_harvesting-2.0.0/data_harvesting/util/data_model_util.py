# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
Utility around dealing with unhide data files on disk and in code. i.e with
LinkedDataObject
"""

import json
import os
import traceback
import time
from pathlib import Path
from typing import Optional
from typing import Union
from urllib.error import HTTPError
from SPARQLWrapper import DIGEST
from SPARQLWrapper import POST
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper.Wrapper import QueryResult

from data_harvesting.aggregator import Aggregator
from data_harvesting.data_model import LinkedDataObject, LDOMetadata
from .rdf_util import Graph


def convert_json_unhide(
    filepath: Union[Path, str],
    *,
    metadata: Optional[LDOMetadata] = None,
    overwrite: bool = False,
    infrmt='jsonld',
    dest: Optional[Path] = None,
):
    """Convert the given jsonld file or all files in a given directory to an unhide data type with some metadata
    this is useful to convert already harvested data on disk without running new versions of the
    harvesters again.

    for now we expect jsonld files only.

    # It may be better to just expect a file list, instead of dir or single file...

    :param filepath: The path to the file or directory, given as path or string.
    :type filepath: Union[Path, str]
    :param metadata: Metadata to be added to each LinkedDataObject
    :type metadata: LDOMetadata(, optional)
    :param overwrite: Should existing files be overwritten? default: False
    :type overwrite: bool
    :param infrmt: The format of the to be read in datafiles have. default: jsonld
    :type infrmt: str
    :param dest: The destination to serialize the new LinkedDataObjects to. default same path as input
    :type dest: Optional[Path]
    """
    if isinstance(filepath, str):
        src = Path(filepath)
    else:
        src = filepath

    if src.is_dir():
        src_files = list(src.glob(f'**/*.{infrmt}'))
        # destination should also be a dir
        if dest is not None:
            if dest.is_file():
                dest = dest.parent
    elif src.is_file():
        src_files = [src]
    else:
        msg = f'Source file path provided for converting to unhide data, does not exists or is not a file or dir: {src}'
        raise ValueError(msg)

    for src_f in src_files:
        with open(src_f, 'rb') as fileo:
            data = json.load(fileo)  # try except this

        ldo = LinkedDataObject(original=data, derived=data)
        ldo.metadata = metadata or ldo.metadata

        # now same linked data Object under same path
        if overwrite:
            name = str(src_f.stem) + '.json'
        else:
            name = str(src_f.stem) + '_unhide' + '.json'
        dest_ = (dest or src_f.parent) / name

        ldo.serialize(destination=dest_)


def apply_aggregator(filepath: Union[Path, str], config: Optional[Path] = None, overwrite: bool = False, dest: Optional[Path] = None):
    """Apply data uplifting to a given unhide file on disk with the current aggregator and its
    configuration. This is useful to migrate unhide data if the configuration changed or if the
    aggregator changed.

    :param filepath: The file path to the LinkedDataObject on disk or folder with more
    :type filepath: Union[Path, str]
    :param config: The path to the configuration file for the Aggregator
    :type config: Optional[Path]
    :param overwrite: Should the new LinkedDataObject overwrite the old one?
    :type overwrite: bool
    :param dest: The destination to serialize the new LinkedDataObjects to. default same path as input
    :type dest: Optional[Path]
    """
    if isinstance(filepath, str):
        src = Path(filepath)
    else:
        src = filepath

    if src.is_dir():
        src_files = list(src.glob('**/*.json'))
    elif src.is_file():
        src_files = [src]
    else:
        msg = f'Source file path provided for uplifting, does not exists or is not a file or dir: {src}'
        raise ValueError(msg)

    agg = Aggregator(config_path=config)
    for src in src_files:
        ldo = LinkedDataObject.from_filename(src)
        try:
            uplifted = agg.apply_to(ldo)
        except Exception as msg:  # rdflib sometimes throws general exceptions..
            print(f'Uplifting of {src} has failed:')
            print(traceback.format_exc())
            # reset to original
            uplifted = ldo

        name = src.name
        if not overwrite:
            name = str(src.stem) + '_uplifted' + '.json'

        dest_file = (dest or src.parent) / name
        uplifted.serialize(destination=dest_file)


def upload_data(
    unhide_data: LinkedDataObject,
    graph_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    username: Optional[str] = None,
    passwd: Optional[str] = None,
    max_tries: int = 5,  # retries in case of disconnect
    max_triples: int = 1000,  # we keep a large safety margin from the 10000 lines because we do not know the
    # length of the query, how it comes to be, i.e how many chars can be in a line...
) -> bool:
    """Upload unhide data to a triple store via a constructed SPARQL update query.

    All kwargs which are not provided are tried to be read from the environment.

    # Comments: This is not so nice yet. There is no pooling for data to be uploaded in bulk.
    The SPARQL query might not be the most efficient way to get the data in.
    Also the logging would be ideally allowed with a token.
    Parsing credentials like this is probably not save.

    :param unhide_data: the LinkedDataObject to upload data from
    :type unhide_data: data_harvesting.LinkedDataObject
    :param graph_name: The graph name to upload the data to
    :type graph_name: Optional[str]
    :param endpoint_url: The url of the SPARQL endpoint to send the data for upload to
    :type endpoint_url: Optional[str]
    :param username: The username to authenticate with
    :type username: Optional[str]
    :param passwd: The password for the username provided
    :type passwd: Optional[str]
    :raises ValueError: If no SPARQL endpoint was given or set otherwise.
    """

    # if connection details are None, try to extract them from the configuration
    # file or environment variables
    if graph_name is None:
        graph_name = os.environ.get('DEFAULT_GRAPH', None)

    if endpoint_url is None:
        endpoint_url = os.environ.get('SPARQL_ENDPOINT', None)

    # This is not save, do better
    if username is None:
        username = os.environ.get('DBA_USER', None)

    if passwd is None:
        passwd = os.environ.get('DBA_PASSWORD', None)

    if endpoint_url is None:
        raise ValueError('The sparql endpoint has to be provided under endpoint_url, or set through the env as SPARQL_ENDPOINT.')

    sparql = SPARQLWrapper(endpoint_url)
    sparql.setHTTPAuth(DIGEST)
    if (username is not None) and passwd is not None:
        sparql.setCredentials(username, passwd)
    sparql.setMethod(POST)
    graph_dic = unhide_data.derived  # jsonld dict
    graph = Graph()
    graph.namespace_manager.bind('schema', 'http://schema.org/')  # this is an unhide specific line,
    # maybe make this an kwarg
    graph.parse(data=json.dumps(graph_dic), format='json-ld')
    all_triples = []
    # Because Virtuoso has a maximum lines of code allowance per default 10000, we have to chop
    # large queries.
    triples = ''
    count = 0
    for sub, pre, obj in graph.triples((None, None, None)):  # pylint: disable=not-an-iterable
        triple = f'{sub.n3()} {pre.n3()} {obj.n3()} . '
        count = count + 1
        if count >= max_triples:  # we keep a safety margin of 10
            all_triples.append(triples)
            triples = ''  # new collection
            count = 0
        triples += triple
    all_triples.append(triples)

    def _upload(sparql, wait_time: int = 0, tries: int = 0):
        """Execute the sparql query in a controlled way"""
        results = None
        time.sleep(wait_time * 60)
        try:
            results = sparql.query()
        except HTTPError as esc:
            xmin = wait_time + 1 + 10 * tries
            tries = tries + 1
            if tries > max_tries:
                print('I failed to upload the given record. Check the connection to the Sparql endpoint.')
                return results
            print(f'HTTPError on upload, I try again in {xmin} min: {esc}')
            _upload(sparql, wait_time=xmin, tries=tries)
        return results

    # create and upload all queries
    for triple_set in all_triples:
        query = 'INSERT IN GRAPH <%s> { %s }' % (graph_name, triple_set)
        sparql.setQuery(query)
        results = _upload(sparql)
        if results is None:
            return False
        if results.response.getcode() == 200:
            print('Your database was successfully updated ... (' + str(len(graph)) + ') triple(s) have been added.')
    return True


def sparql_query(
    query_str: str,
    graph_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    username: Optional[str] = None,
    passwd: Optional[str] = None,
) -> QueryResult:
    """
    Execute a given SPARQL query on a certain graph available at some endpoint.

    All kwargs which are not provided are tried to be read from the environment.

    :param query_str: The SPARQL query as string to be executed on the endpoint
    :type query_str: str
    :param graph_name: The graph name to upload the data to
    :type graph_name: Optional[str]
    :param endpoint_url: The url of the SPARQL endpoint to send the data for upload to
    :type endpoint_url: Optional[str]
    :param username: The username to authenticate with
    :type username: Optional[str]
    :param passwd: The password for the username provided
    :type passwd: Optional[str]
    :raises ValueError: If no SPARQL endpoint was given or set otherwise.
    """
    # if connection details are None, try to extract them from the configuration
    # file or environement variables
    if graph_name is None:
        graph_name = os.environ.get('DEFAULT_GRAPH', None)

    if endpoint_url is None:
        endpoint_url = os.environ.get('SPARQL_ENDPOINT', None)

    # This is not save, do better
    if username is None:
        username = os.environ.get('DBA_USER', None)

    if passwd is None:
        passwd = os.environ.get('DBA_PASSWORD', None)

    if endpoint_url is None:
        raise ValueError('The sparql endpoint has to be provided under endpoint_url, or set through the env as SPARQL_ENDPOINT.')

    sparql = SPARQLWrapper(endpoint_url)
    sparql.setHTTPAuth(DIGEST)
    if (username is not None) and passwd is not None:
        sparql.setCredentials(username, passwd)
    sparql.setMethod(POST)
    sparql.setQuery(query_str)

    # set response type
    results = sparql.query()
    if results.response.getcode() == 200:
        print('The query was successfully executed.')

    return results


def upload_data_filepath(
    filepath: Union[Path, str],
    infrmt: str = 'json',
    graph_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    username: Optional[str] = None,
    passwd: Optional[str] = None,
) -> list:
    """Upload a data from a given filepath, can be a file or a directory tree containing files for upload

    :param filepath: The SPARQL query as string to be executed on the endpoint
    :type filepath: [Path, str]
    :param infrmt: The format of the to be read in data files have. default: json
    :type infrmt: str
    :param graph_name: The graph name to upload the data to
    :type graph_name: Optional[str]
    :param endpoint_url: The url of the SPARQL endpoint to send the data for upload to
    :type endpoint_url: Optional[str]
    :param username: The username to authenticate with
    :type username: Optional[str]
    :param passwd: The password for the username provided
    :type passwd: Optional[str]
    :raises ValueError: If the provided path for the source files, does not exist.
    """
    failures = []
    if isinstance(filepath, str):
        src = Path(filepath)
    else:
        src = filepath

    if src.is_dir():
        src_files = list(src.glob(f'**/*.{infrmt}'))
    elif src.is_file():
        src_files = [src]
    else:
        msg = f'Source file path provided for uploading does not exists or is not a file or dir: {src}'
        raise ValueError(msg)

    for src in src_files:  # TODO Implement Bulk upload....
        unhide_data = LinkedDataObject.from_filename(src)
        success = upload_data(
            unhide_data=unhide_data,
            graph_name=graph_name,
            endpoint_url=endpoint_url,
            username=username,
            passwd=passwd,
        )
        if not success:
            failures.append(src)
    return failures
