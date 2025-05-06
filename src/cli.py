import click
from icecream import ic


@click.group()
@click.pass_context
def doodlebug(ctx):
    ic("Wellcome to doodlebug")



def main():
    doodlebug()
