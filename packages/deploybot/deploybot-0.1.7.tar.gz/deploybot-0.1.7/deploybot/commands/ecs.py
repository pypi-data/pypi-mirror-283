import click
from deploybot.commands.shared import deploy

@click.command()
@click.argument('action')
@click.argument('service_name')
def ecs(action, service_name):
    """Deploy ECS services.

    ACTION: Action to perform (build or deploy).
    SERVICE_NAME: Name of the service to deploy.
    """
    deploy('ecs', action, service_name)
