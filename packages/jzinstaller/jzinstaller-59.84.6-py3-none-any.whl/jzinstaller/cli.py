import click
from code import installjzai

@click.command()
def run():
    """Install JZAI"""
    installjzai()
