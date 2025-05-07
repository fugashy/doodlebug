import click


from .model import model
from .noise import noise
from .updater import updater
from .optimize import optimize


@click.group()
@click.pass_context
def config(ctx):
    pass


commands = [
        model,
        noise,
        updater,
        optimize,
        ]
for c in commands:
    config.add_command(c)
