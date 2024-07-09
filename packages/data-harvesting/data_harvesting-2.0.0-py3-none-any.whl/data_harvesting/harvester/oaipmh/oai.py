# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""Module containing the OAI-PMH Harvester class"""

import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from typing import List

from data_harvesting.harvester.base import BaseHarvester, HarvesterMetadata
from data_harvesting.harvester.oaipmh.convert_harvest import dc_xml_to_schema_org_jsonld
from data_harvesting.util.data_model_util import convert_json_unhide

logger = logging.getLogger('data_harvesting')


class OAIHarvester(BaseHarvester):
    """
    Harvester to collect dublin core xml data from OAI-PMH APIs
    Implements run() function from BaseClass but nothing else for now
    """

    def run(
        self,
        source: str = 'all',
        since: Optional[datetime] = None,
        base_savepath: Optional[Path] = None,
        **kwargs,
    ) -> None:
        since = since or self.get_last_run(source)
        base_savepath = base_savepath or self.outpath
        t = time.localtime()
        start_time = time.strftime('%H:%M:%S', t)
        log_file = f'oai_harvest_{start_time}.log'
        logger.info('OAI Harvester starts. Check %s for details…', log_file)
        count = 0
        base_dir = base_savepath  # / 'oai'
        self.outpath = base_dir
        base_dir_temp = base_savepath / 'temp'
        base_dir_temp.mkdir(parents=True, exist_ok=True)

        harvested_ldo = []
        fails: List[str] = []
        sucs: List[str] = []
        sources = {center_name: center_data for center_name, center_data in self.get_sources().items() if source in (center_name, 'all')}

        for center_name, center_data in sources.items():
            # We only want to convert newly harvested files. Therefore, we harvest files into
            # a temp folder and then move the files at the end.

            output_dir = base_dir_temp / center_name
            metadata_prefix = center_data.get('metadataPrefix', 'oai_dc')
            logger.info('Start OAI harvesting from %s to %s', center_name, output_dir)

            cmd = f"oai-harvest --dir {output_dir} --no-delete --metadataPrefix {metadata_prefix} {center_data['oai_endpoint']}"
            cmd += f' --from {since.strftime("%Y-%m-%d")}' if since is not None else ''
            cmd += f' >> {log_file} 2>&1'

            with subprocess.Popen(cmd, shell=True) as process:
                process.wait()

            # do we need to convert from dublin core?
            convert = center_data.get('convert', True)
            if convert:
                if metadata_prefix == 'oai_dc':
                    dc_xml_to_schema_org_jsonld(output_dir, output_dir)

            # convert to unhide data
            metadata = HarvesterMetadata(
                harvester_class='OAIHarvester',
                provider='center_name',
                preprocess='prov:dc_xml_to_schema_org',
                endpoint=center_data['oai_endpoint'],
            )

            if output_dir.exists():  # It does not, if no records where fetched.
                convert_json_unhide(output_dir, metadata=metadata, overwrite=True)
                # move temp dir files
                target_output_dir = base_dir / center_name
                target_output_dir.mkdir(parents=True, exist_ok=True)
                logger.info(
                    'Moving harvested files from %s to %s',
                    output_dir,
                    target_output_dir,
                )
                for each_file in output_dir.glob('*.*'):
                    count = count + 1
                    target_f = target_output_dir.joinpath(each_file.name)
                    target_f.unlink(missing_ok=True)
                    target_f.parent.mkdir(parents=True, exist_ok=True)
                    each_file.rename(target_f)
                    if each_file.suffix == '.json':
                        harvested_ldo.append(target_f)

                output_dir.rmdir()  # has to be empty
        base_dir_temp.rmdir()
        self.append_last_harvest(harvested_ldo)
        self.append_failures(fails)
        self.append_successes(sucs)
        self.set_last_run(source)
        self.dump_last_harvest(source=source)
        logger.info('OAIHarvester finished! Harvested and processed %i records', count)
