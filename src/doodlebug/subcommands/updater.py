import click


from .wrap import save_as_json


@click.group()
@click.pass_context
def updater(ctx):
    pass


@updater.command()
@save_as_json
@click.option("--weight", type=float, default=0.001)
@click.pass_context
def gauss_newton(ctx, weight):
    ctx.obj["updater"] = {
            "type": "gauss_newton",
            "weight": weight,
            }


