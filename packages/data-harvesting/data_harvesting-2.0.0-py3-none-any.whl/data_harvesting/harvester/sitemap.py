# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""This module contains the pipeline to harvest jsonld data over sitemaps of websites,
similar to what the gleaner software does in the OIH project
"""

import binascii
import json
import logging
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List
from typing import Optional

import advertools as adv
import extruct
import pandas as pd
import progressbar
import requests
from w3lib.html import get_base_url

from data_harvesting.data_model import LinkedDataObject
from data_harvesting.harvester.base import BaseHarvester
from data_harvesting.harvester.base import HarvesterMetadata


logger = logging.getLogger(__name__)


def get_all_sitemaps(url: str) -> pd.DataFrame:
    """From the top sitemap url get all sub urls and parse"""
    sitemap_df = adv.sitemap_to_df(url)  # this might fail, if resource is not available...
    return sitemap_df


def filter_urls(
    sitemap_df: pd.DataFrame,
    since: Optional[datetime] = None,
    match_pattern: Optional[str] = None,
    antimatch_pattern: Optional[str] = None,
) -> pd.DataFrame:
    """Return a list of urls from a given sitemap tree which have been updated since and which optional match a certain pattern

    :param since: str Date
    :param match_pattern: str, regular expression
    """
    sub_df = sitemap_df
    # print(sub_df['loc'][:10])
    if match_pattern is not None:
        # mask = sub_df['loc'].str.contains(match_pattern, case=False, na=False, regex=False)
        mask = [bool(re.match(match_pattern, url)) for url in sub_df['loc']]
        sub_df = sub_df[mask]

    if antimatch_pattern is not None:
        # this does not work yet...
        # sub_df = sub_df[~sub_df['loc'].str.contains(antimatch_pattern, case=False, na=False, regex=False)]
        mask = [not bool(re.match(antimatch_pattern, url)) for url in sub_df['loc']]
        sub_df = sub_df[mask]

    if since is not None:
        # now = date.today()  #now()
        # sub_df = sub_df.between_time(since, now) # this takes only time

        # the dt.date is needed otherwise the timestamp comparison does not work
        sub_df['lastmod_date'] = pd.to_datetime(sub_df['lastmod']).dt.date
        sub_df = sub_df[sub_df['lastmod_date'] > pd.Timestamp(since).date()]

        # if this is turns out to slow, set date the index and do
        # df.loc[start_date:end_date] instead
    return sub_df


def extract_metadata_url(url: str, syntaxes: Optional[List[str]] = None) -> dict:  # , 'microdata', 'opengraph', 'rdfa']):
    """
    # TODO add other format which extruct does not manage
    """
    data: dict = {}
    if syntaxes is None:
        syntaxes = ['dublincore', 'json-ld']

    try:
        req = requests.get(url, timeout=(10, 100))
    except requests.exceptions.ChunkedEncodingError as ex:
        logger.error(f'Invalid chunk encoding {str(ex)}')
        return {syn: [] for syn in syntaxes}
    base_url = get_base_url(req.text, req.url)
    try:
        data = extruct.extract(req.text, syntaxes=syntaxes, base_url=base_url)  # base_rul=base_url,
    except json.JSONDecodeError as err:
        logger.error(f'Could not extract metadata from {url}. {str(err)}')
        return {}

    if len(data.get('json-ld', [])) == 0:
        try:
            req_json = req.json()
        except json.JSONDecodeError:  # requests.exceptions.JSONDecodeError as err:
            return data
        if '@context' in req_json.keys():
            # we assume it is json-ld
            data['json-ld'] = [req_json]

    return data


def transform_url(urls: List[str], url_transforms: Optional[List] = None) -> List[str]:
    """
    Apply given transformation to a url

    currently mainly 'str replace'
    maybe there are better packages to do such things also more general

    for example
    urls_should = ['https://data.fz-juelich.de/api/datasets/export?exporter=schema.org&persistentId=doi:10.26165/JUELICH-DATA/VGEHRD']

    urls = ['https://data.fz-juelich.de/dataset.xhtml?persistentId=doi:10.26165/JUELICH-DATA/VGEHRD']
    transforms = [{'replace' : ('dataset.xhtml?', 'api/datasets/export?exporter=schema.org&')]

    """
    if url_transforms is None:
        url_transforms = []

    new_urls = []
    for url in urls:
        new_url = url
        for transform in url_transforms:
            for key, val in transform.items():
                if key == 'replace':
                    new_url = new_url.replace(val[0], val[1])
        new_urls.append(new_url)

    return new_urls


def harvest_sitemap(
    sitemap: str,
    since: Optional[datetime] = None,
    match_pattern: Optional[str] = r'*/record/\d',  # r ?
    base_savepath: Optional[Path] = None,
    url_transforms: Optional[List[dict]] = None,
    antimatch_pattern: Optional[str] = None,
    skip_existing: Optional[bool] = False,
    unhidedata: bool = False,
):  # , formats=['jsonld']):
    """
    For each url in a sitemap try to extract some metadata of a specified format through different means

    updated since then.
    """
    failed_records = []
    successful_records = []
    record_pointers = []
    sitemap_df = get_all_sitemaps(sitemap)
    record_urls_df = filter_urls(sitemap_df, since=since, match_pattern=match_pattern)
    # print(record_urls_df.keys())
    record_urls = transform_url(record_urls_df['loc'], url_transforms=url_transforms)
    if base_savepath is None:
        base_savepath = Path('.')

    nurls = len(record_urls)
    logger.info(f'Harvesting {nurls} record urls from {sitemap}')
    with progressbar.ProgressBar(max_value=nurls) as pbar:
        for i, record in enumerate(record_urls):
            pbar.update(i)
            # we want to zuse the url as filename, but the / make problems. : also
            # the best solution so far it to encode the url using base64,
            # it can be decoded back with base64.b64decode(filename)
            # binasci.unhexify(filename) (without.json)
            # or https://stackoverflow.com/questions/27253530/save-url-as-a-file-name-in-python
            # filename = f"{record.replace('/', ':')}.json"
            # filename = str(base64.b64encode(record.encode('utf-8')).decode() + ".json")
            filename = binascii.hexlify(record.encode('utf-8')).decode() + '.json'
            # print(filename)
            jsonld_filepath: Path = base_savepath / filename
            if jsonld_filepath.exists() and skip_existing:
                successful_records.append(record)
                record_pointers.append(jsonld_filepath)
                continue
            mdata = extract_metadata_url(record)
            time.sleep(0.1)
            jsonld_md = mdata.get('json-ld', [])
            # if this failed, try to download, json directly
            if len(jsonld_md) == 0:
                logger.info(f'Failed, to retrieve jsonld {record}')
                failed_records.append(record)
                continue

            # Do some basic checks on json-lD

            # store file
            # add some metadata to file
            # jsonld_filepath.write_text(json.dumps(jsonld_md, indent=4))
            # print(jsonld_md)
            if unhidedata:
                metadata = HarvesterMetadata(harvester_class='SitemapHarvester', source_pid=record, sitemap=sitemap)
                ldo = LinkedDataObject(
                    original=jsonld_md[0],
                    derived=jsonld_md[0],
                    patch_stack=[],
                    metadata=metadata,
                )
                ldo.serialize(destination=jsonld_filepath)
            else:
                with open(jsonld_filepath, 'w', encoding='utf-8') as fileo:
                    json.dump(
                        jsonld_md[0],
                        fileo,
                        indent=4,
                        separators=(', ', ': '),
                        sort_keys=True,
                    )
            successful_records.append(record)
            record_pointers.append(jsonld_filepath)

    return successful_records, record_pointers, failed_records


# Todo Lock the URL harvested into a file


class SitemapHarvester(BaseHarvester):
    """This is the Harvester to crawl sitemap.xmls and extract metadata from resulting urls.

    the Urls can be selected according to a given pattern.
    the main target metadata is json-LD which is schema.org conform
    """

    # read in sitemaps which are included in the Knowledge graph
    kg_sitemaps: List['str'] = []

    def run(
        self,
        source='all',
        since: Optional[datetime] = None,
        base_savepath: Optional[Path] = None,
        match_pattern: Optional[str] = None,
        antimatch_pattern: Optional[str] = None,
        url_transforms: Optional[List[dict]] = None,
        **kwargs,
    ):
        """Execute the harvester for a given source, for which the details are specifics are defined
        in the configuration file of the harvester"""
        since = since or self.get_last_run(source)
        base_savepath = base_savepath or self.outpath
        logger.info(f'Sitemap harvester last run: {since}')
        links = []

        failed_records = []
        successful_records = []
        sources = {key: val for key, val in self.get_sources().items() if source in (key, 'all')}
        for center, entry in sources.items():
            if str(base_savepath).endswith('sitemap'):
                base_savepath_c = base_savepath / center
            else:
                base_savepath_c = base_savepath / 'sitemap' / center
            base_savepath_c.mkdir(parents=True, exist_ok=True)
            for sitem_data in entry:
                sitem = sitem_data.get('url', None)
                match_pattern = sitem_data.get('match_pattern', None)
                antimatch_pattern = sitem_data.get('antimatch_pattern', None)
                url_transforms = sitem_data.get('url_transforms', None)
                suc, link, fail = harvest_sitemap(
                    sitem,
                    since=since,
                    base_savepath=base_savepath_c,
                    match_pattern=match_pattern,
                    antimatch_pattern=antimatch_pattern,
                    url_transforms=url_transforms,
                    unhidedata=True,
                )
                failed_records.extend(fail)
                successful_records.extend(suc)
                links.extend(link)

        logger.info(f'The following records failed to be harvested: {failed_records}')

        self.append_last_harvest(links)
        self.append_failures(failed_records)
        self.append_successes(successful_records)
        self.set_last_run(source)
        self.dump_last_harvest(source=source)


# url = 'https://juser.fz-juelich.de/sitemap-index.xml'

# sitemap = get_all_sitemaps(url)
# records = filter_urls(sitemap, match_pattern="*/record/\d")

# print(sitemap)

# sh = SitemapHarvester()
# sh.run(sitemap=url)
