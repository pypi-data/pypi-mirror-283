import click
from __init__ import installjzai

@click.command()
def run():
    """Install JZAI"""
    installjzai()
