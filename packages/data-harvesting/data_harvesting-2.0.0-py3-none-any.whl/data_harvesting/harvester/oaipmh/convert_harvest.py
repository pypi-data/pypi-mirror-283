# -*- coding: utf-8 -*-
"""Provides the method dc_xml_to_schema_org_jsonld for converting a dublin core xml to a schema.org jsonld file."""

import logging
from pathlib import Path

import typer
from lxml import etree

from data_harvesting.harvester.oaipmh.jsonldoutput import JsonldOutput

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
app = typer.Typer(add_completion=True)


@app.command('convert')
def dc_xml_to_schema_org_jsonld(
    input_dir: Path = typer.Option(default=Path('.'), help='Path to the folder that include dc xml files'),
    output_dir: Path = typer.Option(default=Path('.'), help='The output folder to put the converted files in'),
):
    """
    Converts all xml files in an input_dir to a jsonld file.
    All xml tags with a dublin core namespace will be mapped to a suitable schema.org property
    and added to the jsonld file.
    """
    list_dir = []
    if input_dir.exists():
        list_dir = list(input_dir.iterdir())

    file_count = str(len(list_dir))
    logging.info('%s files found in input directory %s.', file_count, input_dir)

    for file in list_dir:
        if not file.suffix == '.xml':
            continue

        filepath = input_dir / file
        with open(filepath, 'rb') as fileo:
            content = fileo.read()

        try:
            xml = etree.fromstring(content)
        except etree.XMLSyntaxError as error:
            logging.error('Error: %s for file %s', str(error), filepath)
            continue

        json_ld = JsonldOutput(xml)
        savepath = output_dir / (filepath.name + '.jsonld')
        json_ld.save(str(savepath))

    logging.info('Conversion from xml dc to schema.org done')
