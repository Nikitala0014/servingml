import click
from build import build
from deploy import deploy

@click.group()
def cli():
    """ServingML Command Line Interface."""
    pass

cli.add_command(build)
cli.add_command(deploy)

if __name__ == "__main__":
    cli()
