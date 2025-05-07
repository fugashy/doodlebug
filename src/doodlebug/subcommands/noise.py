import click
from icecream import ic

from .wrap import save_as_json


@click.group()
@click.pass_context
def noise(ctx):
    pass


@noise.command()
@save_as_json
@click.option(
        "--mean",
        help="Mean of norm. Comma-separated parameters, e.g., 1.,2.",
        default="0.,0.",
        show_default=True)
@click.option(
        "--stddev",
        help="Standard Dev. of norm. Comma-separated parameters, e.g., 1.,2.",
        default="1.,1.",
        show_default=True)
@click.pass_context
def norm(ctx, mean, stddev):
    u"""
    Normal distribution N(mean, stddev)
    """
    mean = [float(v) for v in mean.split(",")]
    stddev = [float(v) for v in stddev.split(",")]
    ctx.obj["noise"] = {
            "model": "norm",
            "params": {
                "mean": mean,
                "stddev": stddev,
                }
            }
    ic(ctx.obj)
