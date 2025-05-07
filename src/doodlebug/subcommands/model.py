import click
from icecream import ic

from .wrap import save_as_json

@click.group()
@click.pass_context
def model(ctx):
    pass


@model.command()
@save_as_json
@click.option("--a", type=float, default=1., show_default=True)
@click.option("--b", type=float, default=1., show_default=True)
@click.pass_context
def linear(ctx, a, b):
    u"""
    f(x) = ax + b
    """
    ctx.obj["model"] = {
            "type": "linear",
            "params": {
                "a": a,
                "b": b,
                }
            }

