# pylint: disable=C0209,C0114,
import subprocess

import click
import uvicorn

from app.core import settings


def run_command(cmd):
    """utility funtion for run shell commands"""
    subprocess.run(cmd, check=True, shell=True)


@click.group
def cli():
    """utility funtion that group all custom command"""


@cli.command()
@click.option("--host", default="127.0.0.1", help="Server host address.")
@click.option("--port", default=8000, help="Port of server.")
@click.option("--reload", default=True, help="Port of server.")
def runserver(host, port, reload):
    """Start a local server"""

    uvicorn.run("app.main:app", host=host, port=port, reload=reload)


@cli.command()
@click.option("--msg", default=None, help="Migration message.")
def makemigrations(msg):
    """Generate migrations file"""
    stmt1 = "alembic revision -m %(msg)s" % {"msg": msg}
    stmt2 = "alembic revision --autogenerate"

    subprocess.run(stmt1 if msg else stmt2, check=True, shell=True)


@cli.command()
def migrate():
    """Update database using latest revision file"""
    cmd = "alembic upgrade head"
    run_command(cmd)


@cli.command()
def psql():
    """run psql terminal for project database"""
    db_url = settings.db_url
    database = db_url.path.replace("/", "")

    cmd = "psql -U %(username)s -h %(host)s -p %(port)s -d %(db)s" % {
        "username": db_url.user,
        "host": db_url.host,
        "port": db_url.port,
        "db": database,
    }
    run_command(cmd)


if __name__ == "__main__":
    # find . -regex '^.*\(__pycache__\|\.py[co]\)$' -delete
    cli()
