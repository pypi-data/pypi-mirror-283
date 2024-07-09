import click
from deploybot.commands.shared import deploy

@click.command(name='lambda')
@click.argument('action')
@click.argument('service_name')
def lambda_(action, service_name):
    """Deploy Lambda services.

    ACTION: Action to perform (deploy).
    SERVICE_NAME: Name of the service to deploy.
    """
    deploy('lambda', action, service_name)
