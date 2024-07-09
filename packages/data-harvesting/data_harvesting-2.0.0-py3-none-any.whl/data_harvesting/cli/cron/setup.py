# -*- coding: utf-8 -*-
#################################################################################################
# This file is part of the data-harvesting package.                                             #
# For copyright and license information see the .reuse/dep5 file                                #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information please visit  https://www.helmholtz-metadaten.de/en                   #
#################################################################################################
"""Command line group for exposed utility"""
import os
import subprocess
from enum import Enum  # If we drop support for Python 3.9 replace with StrEnum

import typer
from crontab import CronTab

app = typer.Typer(add_completion=True)
cron_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cron'))


class CronType(Enum):
    ANACRON = 'anacron'
    CRONTAB = 'crontab'


class CronInterval(Enum):
    HOURLY = 'hourly'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'


@app.command('setup')
def setup_cron(
    cron_type: CronType = typer.Option(
        default=CronType.CRONTAB,
        help='Which cron type should be used for set up up the cron? anacron or normal crontab?',
    ),
    cron_interval: CronInterval = typer.Option(
        default=CronInterval.WEEKLY,
        help='How often should the cron run',
    ),
):
    """
    \b
    Set up a cronjob for the hmc-unhide harverster functionality.
    For this either Anacron or the standard crontab can be used.
    While each user has the latter one, anacron setup needs sudo privileges
    (which are requested automatically while setup).
    But crontab entries are skipped if the machine is not running,
    while anacron guarantees execution.
    Default is crontab.
    """
    if cron_type == CronType.ANACRON:
        symlink = f'/etc/cron.{cron_interval}/hmc-unhide-harvest'

        with subprocess.Popen(f'sudo ln -s {cron_file} {symlink}', shell=True) as process:
            process.wait()

    if cron_type == CronType.CRONTAB:
        with CronTab(user=True) as cron:
            for _ in cron.find_command(cron_file):
                print('Command already exists in crontab. Remove first with `hmc-unhide cron remove`')
                return

            job = cron.new(command=cron_file, comment='HMC UnHIDE Harvester Cronjob')

            if cron_interval == CronInterval.HOURLY:
                job.every(1).hour()

            if cron_interval == CronInterval.DAILY:
                job.every(1).day()

            if cron_interval == CronInterval.WEEKLY:
                job.every(7).day()

            if cron_interval == CronInterval.MONTHLY:
                job.every(1).month()

            if job.is_valid():
                cron.write()


@app.command('list')
def show():
    """
    Shows all set up crons
    """
    print('Crontab:')
    with CronTab(user=True) as crontab:
        for cron in crontab.find_command(cron_file):
            print(cron)

    print('\nAnacron:')
    with subprocess.Popen('ls -1 /etc/cron.*/hmc-unhide-harvest 2> /dev/null', shell=True) as process:
        process.wait()


@app.command()
def remove(
    cron_type: CronType = typer.Option(help='Which cron type should be removed?', default=CronType.CRONTAB),
):
    """
    Removes all crons of a type if exists.
    """
    if cron_type == CronType.ANACRON:
        symlinks = '/etc/cron.*/hmc-unhide-harvest'

        with subprocess.Popen(f'sudo rm -r {symlinks}', shell=True) as process:
            process.wait()

    if cron_type == CronType.CRONTAB:
        with CronTab(user=True) as cron:
            cron.remove_all(command=cron_file)
