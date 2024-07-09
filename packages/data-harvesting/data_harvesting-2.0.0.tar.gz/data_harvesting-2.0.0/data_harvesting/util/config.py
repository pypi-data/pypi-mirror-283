# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
Contains methods around the configuration file for the data pipelines.
This includes loading from a given file or default as well as validation of it.
"""

import yaml
from pathlib import Path
from typing import Optional
from data_harvesting.model_core import UnhideConfig

PKG_ROOT_DIR = Path(__file__).parent.parent.resolve()


def get_config_path() -> Path:
    """
    Return the path to the default configuration file (config.yaml) within this
    repository for the data pipeline.

    :return: The default path to the configuration file
    :rtype: pathlib.Path
    """

    config_path = PKG_ROOT_DIR / 'configs' / 'config.yaml'

    return config_path


def get_config(config_path: Optional[Path] = None) -> dict:
    """Load a given configuration file and return the configuration.

    This also validates the configuration file on read into a pydantic data model
    for it.

    :param config_path: The path pointing to a configuration file
    :type config_path: pathlib.Path
    :return: A dictionary containing the loaded yaml config
    :rtype: dict
    """

    if config_path is None:
        config_path = get_config_path()

    config = {}
    with open(config_path, 'r', encoding='utf-8') as fileo:
        config = yaml.load(fileo, Loader=yaml.FullLoader)
    config = UnhideConfig(**config).dict()  # Validation happens here

    return config


def validate_config_file(config_path: Optional[Path] = None) -> None:
    """Validate a given configuration file

    :param config_path: The path pointing to a configuration file
    :type config_path: pathlib.Path
    """
    get_config(config_path)  # validation happens on read in
