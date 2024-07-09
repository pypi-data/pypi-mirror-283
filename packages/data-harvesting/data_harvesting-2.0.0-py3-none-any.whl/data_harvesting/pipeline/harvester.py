# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""
This module contains all harvester flows
"""
from datetime import datetime
from pathlib import Path
from typing import Optional

from prefect import flow
from prefect import get_run_logger
from prefect import task
from prefect.artifacts import create_markdown_artifact
from data_harvesting.harvester import HARVESTER_CLASSMAP as harvester_classmap


# async
@flow(log_prints=True, persist_result=True, flow_run_name='harvest-{harvester}')
def run_harvester(harvester: str = 'all', out: Optional[Path] = None, config: Optional[Path] = None):
    """
    A prefect flow to run a single or all harvesters
    """
    logger = get_run_logger()
    logger.info(f'Starting harvesting: {harvester}!')
    all_resources = []
    if out is None:
        out = Path('.')
    # subflows = []
    if harvester == 'all':
        # rekursion
        for harvester_ in list(harvester_classmap.keys()):
            out_harvester = out / f'{harvester_}'
            resource = run_harvester(harvester=harvester_, out=out_harvester, config=config)  # , return_state=True)
            all_resources.extend(resource)  # does this stop the interpreter?
            # subflows.append(run_harvester(harvester=harvester_, out=out, config=config, return_state=True))

    else:
        # since we want every resource to be a specific task, we have to add some logic from the harvester
        # concurrent runs of harvesters might run into problems from the last run file persistence...
        # therefore ggf persist since somehow else, or change to a source based one
        # resource = harvest_source.submit(source=harvester, out=out, config=config)
        # all_resources.extend(resource.result())
        out_harvester = out / f'{harvester}'
        harvester_c = harvester_classmap[harvester](outpath=out_harvester, config_path=config)
        sources = harvester_c.sources
        for key, val in sources.items():
            since = harvester_c.get_last_run(key)
            # subflows.append(harvest_source(harvester=harvester, source=key, out=out, config=config, since=since))
            resource = harvest_source.submit(harvester=harvester, source=key, out=out_harvester, config=config, since=since)
            all_resources.extend(resource.result())
    # await asyncio.gather(*subflows)
    # for subf in subflows:
    #    all_resources.extend(subf.result())

    logger.info(f'Harvesting from: {harvester} Done!')
    return all_resources


@task(persist_result=True, log_prints=True, task_run_name='harvest-{harvester}-task-{source}')
def harvest_source(
    source: str,
    out: Path,
    harvester: str = 'all',
    config: Optional[Path] = None,
    since: Optional[datetime] = None,
):
    """Harvest from a single source in the config, and log it as a prefect task
    for each source there will be a new harvester initialized.
    """
    logger = get_run_logger()
    # Problem and thoughts:
    # this is a little bit bend to get it all into a task without parsing a harvester class
    # so we initialize a new one from the same config and out path
    # there will be a problem with 'last run files' since they are harvester specific and not source
    # specific. therefore maybe parse since/last run to this function and then set it to the class?
    # Also the run interface of the harvesters is not harmonized? for source since and base_savepath?
    harvester_c = harvester_classmap[harvester](outpath=out, config_path=config)
    # overwrite since
    if since is not None:
        harvester_c.set_last_run(source, time=since)
    logger.info(f'Harvesting subtask from: {source}!')
    config_str = harvester_c.get_config()
    sources = harvester_c.get_sources()

    markdown_config = f""" # Harvester run overview


    ## General information:
    Configuration file that the {harvester} harvester ran with.
    Harvesting data from {source} since: {since}. The data is stored under {out}.

    ## Sources the harvester picked up:

    {sources}

    ## Full Configuration for harvester run:

    {config_str}


    """

    create_markdown_artifact(
        key=f'{harvester}-harvester-config',
        markdown=markdown_config,
        description=f'Configuration file that the {harvester} harvester ran with. Harvesting data from {source} since: {since}. The data is stored under {out}.',
    )
    harvester_c.run(source=source, since=since, base_savepath=out)
    logger.info(f'Harvesting subtask from: {source} done!')
    last_harvest = harvester_c.last_harvest
    nfiles = len(last_harvest)
    fails = harvester_c.get_failures()
    nfails = len(fails)
    success = harvester_c.get_successes()
    nsucs = len(success)

    last_harvest_dump = harvester_c.get_last_harvest_dump_path()
    # maybe we would like to store the PIDs
    markdown_results = f"""# Results report
    Last harvest file stored under: {last_harvest_dump}
    Also it is stored by prefect, for this check the persistent data link of the file.

    {nfails} Failures: {fails}
    {nsucs} Successes: {success}

    """
    create_markdown_artifact(
        key=f'{harvester}-harvester-{nfiles}-results',
        markdown=markdown_results,
        description=f'Results of the last harvest of {harvester} harvester from source. Data stored under {out}, harvested {nfiles} records since: {since}. Of these nfailed and nsuc succeeded.',
    )
    return last_harvest
    # return ['my_test_file.json', 'my_test_file2.json']
