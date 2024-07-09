# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
This module contains util and a class to harvest metadata from indico instances
"""

import binascii
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List
from typing import Optional

import extruct
import progressbar
import requests
from w3lib.html import get_base_url

from data_harvesting.data_model import LinkedDataObject
from data_harvesting.harvester.base import BaseHarvester, HarvesterMetadata

logger = logging.getLogger(__name__)


def harvest_indico(
    url_in: str,
    categories: Optional[list] = None,
    api_token: Optional[str] = None,
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
        base_savepath = Path('.') / 'indico'
    base_savepath.mkdir(parents=True, exist_ok=True)

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive',
    }

    if since is None:
        now = datetime.now()
        since_date = str(int(now.year) - 10) + '-01-01'
        to_date = str(int(now.year) + 10) + '-01-01'
    else:
        since_date = since.isoformat().split('T')[0]
        to_date = str(int(since.year) + 3) + '-01-01'

    categories = categories or []
    for cat in categories:
        request_cat = f'/export/categ/{cat}' + f'.json?from={since_date}&to={to_date}&pretty=yes'
        req = requests.get(url_in + request_cat, headers=headers, timeout=(10, 60))
        events = req.json().get('results', [])
        logger.info(f'Harvesting {len(events)} events from Indico {url_in} using {url_in + request_cat}')
        with progressbar.ProgressBar(max_value=len(events)) as pbar:
            for i, event in enumerate(events):
                pbar.update(i)
                url_ev = event.get('url')
                if unhidedata:
                    filename = binascii.hexlify(url_ev.encode('utf-8')).decode() + '.json'
                else:
                    filename = binascii.hexlify(url_ev.encode('utf-8')).decode() + '.jsonld'
                jsonld_filepath: Path = base_savepath / filename
                if jsonld_filepath.exists() and skip_existing:
                    successful_records.append(url_ev)
                    record_pointers.append(jsonld_filepath)
                    continue
                time.sleep(0.5)
                req = requests.get(url_ev, timeout=(10, 60))
                base_url_ex = get_base_url(req.text, req.url)
                json_ld = extruct.extract(req.text, syntaxes=['json-ld'], base_url=base_url_ex).get('json-ld')[-1]
                keywords = event.get('keywords', None)
                if keywords:
                    json_ld['keywords'] = keywords
                json_ld['@id'] = url_ev

                time.sleep(0.01)
                if unhidedata:  # store as linked data.
                    metadata = HarvesterMetadata(harvester_class='IndicoHarvester', source_pid=url_ev, provider=url_in)
                    ldo = LinkedDataObject(
                        original=json_ld,
                        derived=json_ld,
                        patch_stack=[],
                        metadata=metadata,
                    )
                    ldo.serialize(destination=jsonld_filepath)
                else:  # just dump what was found
                    with open(jsonld_filepath, 'w', encoding='utf-8') as fileo:
                        json.dump(
                            json_ld,
                            fileo,
                            indent=4,
                            separators=(', ', ': '),
                            sort_keys=True,
                        )
                successful_records.append(url_ev)
                record_pointers.append(jsonld_filepath)

    return successful_records, record_pointers, failed_records


class IndicoHarvester(BaseHarvester):
    """This is the Harvester to crawl indico instances and extract metadata from resulting urls.

    the Urls are retrieved from an API.
    if no token is there, a certain number range is crawled.
    """

    # for know we just allow these, others could be possible
    # i.e get all child and parent organizations also
    def __init__(self, outpath=Path('.'), **kwargs):
        if isinstance(outpath, str):
            outpath = Path(outpath)
        super().__init__(outpath=outpath, **kwargs)

    def get_sources(self):
        # sources is set on init from a provided or default config file
        return self.sources

    def run(
        self,
        source: str = 'all',
        since: Optional[datetime] = None,
        base_savepath: Optional[Path] = None,
        **kwargs,
    ):
        """Execute the harvester for a given indico instance or all"""
        since = since or self.get_last_run(source)
        base_savepath = base_savepath or self.outpath

        fails = []
        links = []
        sucs = []
        logger.info(f'IndicoHarvester last run: {since}')
        sources = {key: val for key, val in self.get_sources().items() if source in (key, 'all')}

        for key, val in sources.items():
            url_in = val.get('url', None)
            cats = val.get('categories', [])
            token = val.get('token', [])
            logger.info(f'Harvesting Indico instance {key} {url_in}')
            base_savepath1 = base_savepath / key
            suc, link, fail = harvest_indico(url_in, categories=cats, base_savepath=base_savepath1, since=since, api_token=token)
            fails.extend(fail)
            sucs.extend(suc)
            links.extend(link)

        logger.info(f'Failed to harvest: {fails}')

        self.append_last_harvest(links)
        self.append_failures(fails)
        self.append_successes(sucs)
        self.set_last_run(source)
        self.dump_last_harvest(source=source)
