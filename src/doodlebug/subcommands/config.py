import click


from .data import data
from .noise import noise

@click.group()
@click.pass_context
def config(ctx):
    pass


commands = [
        data,
        noise,
        ]
for c in commands:
    config.add_command(c)
