import click


from .wrap import save_as_json


@click.command()
@save_as_json
@click.option("--start", "-s", type=float, default=0.)
@click.option("--step", "-st", type=float, default=0.1)
@click.option("--num", "-n", type=int, default=100)
@click.option("--tolerance", type=float, default=0.00001)
@click.pass_context
def optimize(ctx, start, step, num, tolerance):
    ctx.obj["optimize"] = {
            "params": {
                "start": start,
                "step": step,
                "num": num,
                "tolerance": tolerance,
            }
        }
