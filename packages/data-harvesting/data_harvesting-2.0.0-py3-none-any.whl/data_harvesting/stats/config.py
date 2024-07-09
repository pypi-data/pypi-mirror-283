# -*- coding: utf-8 -*-

from os import environ
from data_harvesting.stats.models import ReportItem
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Environment variables
LOG_PATH = environ.get('LOG_PATH', './logs/access.log')

# Git repository related environment variables
REPOSITORY_URL = environ.get('REPOSITORY_URL', None)
REPOSITORY_BRANCH = environ.get('REPOSITORY_BRANCH', 'main')
GIT_USERNAME = environ.get('GIT_USERNAME', None)
GIT_EMAIL = environ.get('GIT_EMAIL', None)
GIT_TOKEN = environ.get('GIT_TOKEN', None)

# boolean debug value
DEBUG = environ.get('DEBUG', 'false').lower() == 'true'

# Constants
DB_NAME = Path('/opt/hifis-data/hifis_stats.db')
GIT_FOLDER = Path('hifis-stats')
REPORT_FILE = GIT_FOLDER / Path('stats/statistics.csv')

REPORT_ITEMS = [
    ReportItem(
        name='Search Index Page Requests',
        domain_name='search.unhide.helmholtz-metadaten.de',
        url_patterns=[r'^\/$'],
    ),
    ReportItem(
        name='Search Requests',
        domain_name='api.unhide.helmholtz-metadaten.de',
        url_patterns=[r'^\/search*', r'^\/api\/search*'],
    ),
    ReportItem(
        name='Sparql Index Page Requests',
        domain_name='sparql.unhide.helmholtz-metadaten.de',
        url_patterns=[r'^\/$', r'^\/sparql$'],
    ),
    ReportItem(
        name='Sparql Requests',
        domain_name='sparql.unhide.helmholtz-metadaten.de',
        url_patterns=[r'^\/\?default\-graph\-uri*'],
    ),
]
