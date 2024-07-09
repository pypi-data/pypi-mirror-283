# -*- coding: utf-8 -*-
import typer
from data_harvesting.stats import save_logs, report_logs, register_flows

app = typer.Typer(add_completion=True)


@app.command('record')
def record():
    """Save the nginx log to the database."""
    save_logs()


@app.command('report')
def report():
    """Report the nginx logs and stats in the database to the specified report git repository."""
    report_logs()


@app.command('register')
def register():
    """Register a cron job in prefect for the nginx log execution."""
    register_flows()
