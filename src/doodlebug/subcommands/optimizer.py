import click


from .wrap import save_as_json


@click.group()
@click.option("--tolerance", type=float, default=0.00001)
@click.pass_context
def optimizer(ctx, tolerance):
    ctx.obj["optimizer"] = {
            "tolerance": tolerance,
            }


@optimizer.command()
@save_as_json
@click.pass_context
def test(ctx):
    pass

