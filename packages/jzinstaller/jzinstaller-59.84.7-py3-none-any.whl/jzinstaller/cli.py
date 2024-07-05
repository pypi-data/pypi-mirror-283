import click
import codepyfile as code

@click.command()
def run():
    """Install JZAI"""
    code.installjzai()
