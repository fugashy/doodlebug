import click
from icecream import ic
ic.configureOutput(
        prefix="doodlebug | ",
        includeContext=False)

from .subcommands.config import config
from .subcommands.show import show
from .core.optimize import (
        optimize as opt,
        optimize_graph as opt_graph,
        )


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


@doodlebug.command()
@click.pass_context
def optimize(ctx):
    opt(ctx.obj)


@doodlebug.command()
@click.argument("graph_filepath", type=str)
def optimize_graph(graph_filepath):
    opt_graph(graph_filepath)


def main():
    commands = [
            config,
            show,
            ]
    for c in commands:
        doodlebug.add_command(c)
    doodlebug()
