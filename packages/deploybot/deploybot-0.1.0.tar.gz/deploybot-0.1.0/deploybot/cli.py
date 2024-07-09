import click
from deploybot.commands.configure import configure
from deploybot.commands.ecs import ecs
from deploybot.commands.lambda_ import lambda_
from deploybot.utils.version import get_version

VERSION = get_version()

@click.group()
@click.version_option(VERSION, '-v', '--version', prog_name='deploybot')
def cli():
    pass

cli.add_command(configure)
cli.add_command(ecs)
cli.add_command(lambda_)

if __name__ == '__main__':
    cli()
