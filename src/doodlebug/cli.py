import click
from icecream import ic
ic.configureOutput(
        prefix="doodlebug | ",
        includeContext=False)

from .subcommands.config import config


u"""
doodlebug
    data linear 
"""


@click.group()
@click.option("--config_filepath", "-c", type=str, default="/tmp/doodlebug.json", show_default=True)
@click.pass_context
def doodlebug(ctx, config_filepath):
    ic("Wellcome")
    ctx.ensure_object(dict)
    ctx.obj["config_filepath"] = config_filepath


def main():
    commands = [
            config,
            ]
    for c in commands:
        doodlebug.add_command(c)
    doodlebug()
