# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""Cli command to uplift unhide data"""

from pathlib import Path
from typing import List
from typing import Optional

import typer
from rich.console import Console

from data_harvesting.util.data_model_util import apply_aggregator

console = Console()
app = typer.Typer(add_completion=True)


@app.command('uplift')
def uplift(filenames: List[Path], config: Optional[Path] = None, overwrite: bool = True) -> None:
    for filename in filenames:
        apply_aggregator(filename, config=config, overwrite=overwrite)
