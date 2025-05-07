import click


from .data import data
from .noise import noise
from .updater import updater
from .optimizer import optimizer


@click.group()
@click.pass_context
def config(ctx):
    pass


commands = [
        data,
        noise,
        updater,
        optimizer,
        ]
for c in commands:
    config.add_command(c)
