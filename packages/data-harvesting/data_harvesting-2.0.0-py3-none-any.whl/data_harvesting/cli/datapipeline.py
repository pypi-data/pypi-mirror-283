# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
This module contains all cli function for the data pipeline
"""

from pathlib import Path

import typer
from rich.console import Console
from typing import List
from typing import Optional
from data_harvesting import get_config_path
from data_harvesting.pipeline import run_pipeline, run_harvester, run_uploader, run_indexer, run_aggregator
from data_harvesting.pipeline.pipeline import register_pipeline

console = Console()
app = typer.Typer(add_completion=True)


@app.command()
def register(
    name: str = typer.Option('all', help='The harvester to execute.'),
    out: Path = typer.Option(Path('.').resolve(), help='The folder path where to save stuff'),
    config: Path = typer.Option(get_config_path()),
    uplifting: bool = typer.Option(True, help='Uplift the harvested files.'),
    index: bool = typer.Option(True, help='Index files into solr.'),
    upload: bool = typer.Option(True, help='Upload files into triple store.'),
    time_interval: str = typer.Option('0 0 * * SAT', help='The cron job interval to set. Default is weekly.'),
    label: str = typer.Option('', help='An additional label for the deployment name, helpful to have several deployments.'),
) -> None:
    """Register a cron job in prefect for the pipeline execution."""
    register_pipeline(
        time_interval=time_interval, harvester=name, out=out, config=config, uplifting=uplifting, upload=upload, index=index, label=label
    )


@app.command()
def run(
    name: str = typer.Option('all', help='The harvester to execute.'),
    out: Path = typer.Option(Path('.').resolve(), help='The folder path where to save stuff'),
    config: Path = typer.Option(get_config_path()),
    uplifting: bool = typer.Option(True, help='Uplift the harvested files.'),
    index: bool = typer.Option(True, help='Index files into solr.'),
    upload: bool = typer.Option(True, help='Upload files into triple store.'),
) -> None:
    """Run the datapipeline (through prefect) for a certain source type. if all, it is run for every source type."""
    run_pipeline(harvester=name, out=out, config=config, uplifting=uplifting, upload=upload, index=index)


@app.command('harvest')
def run_harvest(
    name: str = typer.Option('all', help='The harvester to execute.'),
    out: Path = typer.Option(Path('.').resolve(), help='The folder path where to save stuff'),
    config: Path = typer.Option(get_config_path()),
) -> None:
    """Run the harvester (through prefect) for a certain source type. If all, it is run for every source type."""
    res = run_harvester(harvester=name, out=out, config=config)
    nres = len(res)
    print(f'Harvested {nres} resources.')


@app.command('uplift')
def run_uplift(
    files: List[Path],
    source: str = typer.Option('non-specified', help='The source this was from for metadata annotation.'),
    config: Path = typer.Option(get_config_path()),
) -> None:
    """Run the uplifter (through prefect) on a given list of files."""
    nfiles = len(files)
    run_aggregator(files=files, nfiles=nfiles, source=source, config=config)


@app.command('index')
def run_index(
    files: List[Path],
    config: Optional[Path] = typer.Option(None, help='Path pointing to the config file.'),
    source: str = typer.Option('non-specified', help='The source this was from for metadata annotation.'),
    fl_reindex: bool = typer.Option(False, help='Should an existing record be reindexed?.'),
    fail: bool = typer.Option(False, help='Should the indexer fail in the case of an exception?'),
) -> None:
    """Run the indexer (through prefect) for a given list of files."""
    nfiles = len(files)
    run_indexer(files=files, nfiles=nfiles, source=source, fl_reindex=fl_reindex, fail=fail, config=config)


@app.command('upload')
def run_upload(
    files: List[Path],
    source: str = typer.Option('all', help='The source this was from for metadata annotation.'),
    config: Optional[Path] = typer.Option(None, help='Path pointing to the configuration file.'),
    infrmt: str = typer.Option('json', help='The input format to look for.'),
    graph_name: Optional[str] = typer.Option(None, help='The graph url or name to be uploaded to. This can also be read from the env.'),
    endpoint_url: Optional[str] = typer.Option(None, help='The url of the SPARQL endpoint. This can also be read from the env.'),
    username: Optional[str] = typer.Option(
        None, help='The user name with write access to the endpoint. This can also be read from the env.'
    ),
    passwd: Optional[str] = typer.Option(None, help='The password of the user. This can also be read from the env.'),
) -> None:
    """Run the uploader (through prefect) for a given list of files."""
    nfiles = len(files)
    run_uploader(
        files=files,
        source=source,
        config=config,
        nfiles=nfiles,
        infrmt=infrmt,
        graph_name=graph_name,
        endpoint_url=endpoint_url,
        username=username,
        passwd=passwd,
    )
