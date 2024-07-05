import os

import click

from wscli.clis import auth
from wscli.clis import config
from wscli.clis import ml
# from wscli.clis import organizations


from wscli.config import ConfigStorer
from wscli.config import WsConfig, pass_config
from pydantic import TypeAdapter

@click.group()
@click.option(
    "--home",
    envvar="WSCLI_HOME",
    default=lambda: os.environ.get("HOME") + "/.wscli")
@click.pass_context
def cli(context, home: str):
    storer = ConfigStorer(home=home)
    storer.setup()
    context.obj = WsConfig.load(storer)

@cli.command()
@pass_config
def show_config(config: WsConfig):
    click.echo(TypeAdapter(WsConfig).dump_json(config, indent=2))

cli.add_command(auth.cli, name="auth")
cli.add_command(config.cli, name="config")
cli.add_command(ml.cli, name="ml")
# cli.add_command(organizations.cli, name="org")
