# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
This module contains util and a class to harvest metadata from rss and atom feeds
"""

import binascii
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List
from typing import Optional

import atoma
import extruct
import progressbar
import requests
from pytz import UTC as Utc
from w3lib.html import get_base_url

from data_harvesting.data_model import LinkedDataObject
from data_harvesting.harvester.base import BaseHarvester, HarvesterMetadata

logger = logging.getLogger(__name__)


def convert_micro_jsonld(data):
    """Dirty converter of some microdata of a schema.org type to jsonld"""
    json_ld = {'@context': 'https://schema.org'}
    for data_ in data:
        type_ = data_.get('type')
        if 'schema.org' not in type_:
            return None

        json_ld['@type'] = type_.split('schema.org/')[-1]
        properties = data_.get('properties', {})
        json_ld['title'] = properties.get('title', '')
        json_ld['description'] = properties.get('description', '')
    return json_ld


def parse_feed(content, feed_type: Optional[str]):
    """Parse the byte content from a request depending on the type of the feed

    :param feed: [description]
    :type feed: [type]
    :param feed_type: [description]
    :type feed_type: str
    """
    feed_type = feed_type or 'atom'
    if feed_type == 'atom':
        feed = atoma.parse_atom_bytes(content)
    elif feed_type == 'rss':
        feed = atoma.parse_rss_bytes(content)
    else:
        raise ValueError(f'Feedtype. {feed_type} is not supported, only rss or atom feeds are.')
    return feed


def harvest_feed(
    url_in: str,
    feed_type: Optional[str] = None,
    since: Optional[datetime] = None,
    base_savepath: Optional[Path] = None,
    skip_existing: Optional[bool] = True,
    unhidedata: bool = True,
):
    """
    For each pid related to the ror identifier, down load all metadata records

    updated since then.
    """
    failed_records: List[str] = []
    successful_records: List[str] = []
    record_pointers: List[Path] = []

    if base_savepath is None:
        base_savepath = Path('.') / 'feed'
    base_savepath.mkdir(parents=True, exist_ok=True)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/xml',
        'Connection': 'keep-alive',
    }
    req = requests.get(url_in, headers=headers, timeout=(10, 60))
    feed = parse_feed(req.content, feed_type)

    if since is None:
        since = datetime.now()
        since = datetime.fromisoformat(str(int(since.year) - 10) + '-01-01')
    since = since.replace(tzinfo=Utc)

    events = feed.entries
    logger.info(f'Harvesting {len(events)} records from Feed {url_in}')
    with progressbar.ProgressBar(max_value=len(events)) as pbar:
        for i, event in enumerate(events):
            pbar.update(i)
            # atom specific
            url_ev = event.id_
            modified = event.updated.replace(tzinfo=Utc)

            if since > modified:
                continue

            if unhidedata:
                filename = binascii.hexlify(url_ev.encode('utf-8')).decode() + '.json'
            else:
                filename = binascii.hexlify(url_ev.encode('utf-8')).decode() + '.jsonld'
            jsonld_filepath: Path = base_savepath / filename
            if jsonld_filepath.exists() and skip_existing:
                successful_records.append(url_ev)
                record_pointers.append(jsonld_filepath)
                continue
            time.sleep(0.3)
            req2 = requests.get(url_ev, timeout=(10, 60))
            base_url_ex = get_base_url(req2.text, req2.url)
            syntaxes = ['json-ld', 'microdata', 'rdfa']
            data = extruct.extract(req2.text, syntaxes=syntaxes, base_url=base_url_ex)
            json_ld = data.get('json-ld')
            if json_ld:
                json_ld = json_ld[-1]
            else:
                # for now dirty microdata parse into jsonld
                micro = data.get('microdata')
                json_ld = convert_micro_jsonld(micro)
                logger.warning(f'No json ld data found for {url_ev}.')
                if json_ld is None:
                    continue
            if json_ld.get('@id', None) is None:
                json_ld['@id'] = url_ev
            time.sleep(0.01)
            mdata = json_ld
            if unhidedata:  # store as linked data.
                metadata = HarvesterMetadata(harvester_class='FeedHarvester', source_pid=url_ev, provider=url_in)
                ldo = LinkedDataObject(original=mdata, derived=mdata, patch_stack=[], metadata=metadata)
                ldo.serialize(destination=jsonld_filepath)
            else:  # just dump what was found
                with open(jsonld_filepath, 'w', encoding='utf-8') as fileo:
                    json.dump(mdata, fileo, indent=4, separators=(', ', ': '), sort_keys=True)
            successful_records.append(url_ev)
            record_pointers.append(jsonld_filepath)
    return successful_records, record_pointers, failed_records


class FeedHarvester(BaseHarvester):
    """This is the Harvester to crawl a feed and extract metadata from resulting urls."""

    def run(
        self,
        source='all',
        since: Optional[datetime] = None,
        base_savepath: Optional[Path] = None,
        **kwargs,
    ):
        """Execute the harvester for a given feed instance or all"""
        since = since or self.get_last_run(source)
        base_savepath = base_savepath or self.outpath

        fails = []
        links = []
        sucs = []
        logger.info(f'FeedHarvester last run: {since}')
        sources = {key: val for key, val in self.get_sources().items() if source in (key, 'all')}

        for key, val in sources.items():
            urls_in = val.get('urls', None)
            feed_types = val.get('types', None)  # default is atom
            base_savepath1 = base_savepath / key
            for i, url_in in enumerate(urls_in):
                logger.info(f'Harvesting Feed {key} {url_in}')
                feed_type = None if feed_types is None else feed_types[i]
                suc, links, fail = harvest_feed(url_in, feed_type=feed_type, base_savepath=base_savepath1, since=since)
                fails.extend(fail)
                sucs.extend(suc)

        logger.info(f'Failed to harvest: {fails}')
        print(f'Harvested last harvest: {links}')
        self.append_last_harvest(links)
        self.append_failures(fails)
        self.append_successes(sucs)
        self.set_last_run(source)
        self.dump_last_harvest(source=source)
