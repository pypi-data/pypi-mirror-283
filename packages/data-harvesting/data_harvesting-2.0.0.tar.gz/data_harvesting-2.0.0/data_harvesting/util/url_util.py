# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
module containing utlitity to deal with urls and dois
"""

from hashlib import sha256
from typing import Optional
from urllib.parse import urlparse, quote_plus
import requests


def get_url_from_doi(doi: str) -> Optional[str]:
    """
    :param doi (str): DOI in the form '10.5290/200360144' (example) not the full url link

    :return url (str): if resolveable, otherwise None.
    """
    url = None
    urls = []
    handle = f'https://doi.org/api/handles/{doi}'

    # Handle errors
    req = requests.get(handle, timeout=(3, 60))
    if req.status_code != 200:
        # print(req.status_code)
        return None

    res_json = req.json()
    if 'values' in res_json.keys():
        for val in res_json['values']:
            if val.get('type') == 'URL':
                urls.append(val['data']['value'])
        if len(urls) > 0:
            url = urls[0]

    return url


# test
# print(get_url_from_doi('10.5290/200360144'))
# https://odin.jrc.ec.europa.eu/alcor/DOIDisplay.html?p_RN5=200360144


def get_domain_from_url(url: str) -> str:
    """Extract the base domain link from a given url

    :param url (str): example https://archive.materialscloud.org/record/2021.134
    :return domain (str): example https://archive.materialscloud.org
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc


def clean_pid(pid: str) -> str:
    """Return only relevent part of pid

    http://dx.doi.org/10.5290/207200009 -> 10.5290/207200009
    """
    # Does not work for https://doi.org/10.24435/materialscloud:nq-ht
    # returns /alcor/DOIDisplay.html
    # parsed_url = urlparse(url)
    # return parsed_url.path
    clean = ''.join(pid.split('//')[1:])
    cleaned = ''.join(part + '/' for part in clean.split('/')[1:])
    cleaned = cleaned.strip('/')
    return cleaned


def hash_url(url: str) -> str:
    """Has a given url to a unique but hex string"""
    url_hash = sha256(url.encode()).hexdigest()
    return url_hash


def conditional_encode_url(url: str, forbidden_chars: str = '<>" {}|\^`', encoding: Optional[str] = None, safe: str = '/:,') -> str:
    """Encode a url, but only if it contains one of the forbidden chars"""
    new_url = url
    for s in url:
        if s in forbidden_chars:
            new_url = quote_plus(url, encoding=encoding, safe=safe)
            break
    return new_url


def encode_url(url: str, encoding: Optional[str] = None, safe: str = '/:,') -> str:
    """Encode a given url with a given encoding"""
    encoded_url = quote_plus(url, encoding=encoding, safe=safe)
    return encoded_url


def make_url_save(data: dict) -> dict:
    """Make all urls in dict save"""
    for key, val in data.items():
        if isinstance(val, str):
            if val.startswith('http'):
                new_val = conditional_encode_url(val)
                data[key] = new_val
        elif isinstance(val, dict):
            data[key] = make_url_save(val)  # ! recursion
        elif isinstance(val, list):
            new_list = []
            for item in val:
                if isinstance(item, str):
                    if item.startswith('http'):
                        new_val = conditional_encode_url(item)
                        new_list.append(new_val)
                elif isinstance(val, dict):
                    new_list.append(make_url_save(item))  # ! recursion
                else:
                    new_list.append(item)
            data[key] = new_list
    return data
