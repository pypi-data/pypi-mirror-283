import click
import subprocess
from deploybot.utils.aws import get_aws_account_id
from deploybot.utils.config import get_config, save_config
from pathlib import Path
import os
from InquirerPy import inquirer

@click.command()
def configure():
    """Configure AWS account ID and set the environment."""
    aws_account_id = click.prompt('Enter your AWS account ID')
    actual_aws_account_id = get_aws_account_id()

    if actual_aws_account_id != aws_account_id:
        click.echo("AWS account ID does not match the current AWS CLI configuration.")
        return

    environment = inquirer.select(
        message="Select environment:",
        choices=["staging", "production"]
    ).execute()

    base_path = click.prompt('Enter the base path of the project')

    os.chdir(base_path)
    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()

    if environment == 'staging' and branch == 'master':
        click.echo("Warning: Selected staging environment but the branch is master.")
        return
    elif environment == 'production' and branch != 'master':
        click.echo("Warning: Selected production environment but the branch is not master.")
        return

    click.echo(f"You added this account ID: {aws_account_id}")
    click.echo(f"This is the environment: {environment}")
    click.echo(f"This is the path: {base_path}")
    click.echo(f"This is the branch: {branch}")

    confirm = click.confirm("Are you sure to save these settings?")
    if confirm:
        save_config(aws_account_id, environment, base_path, branch)
        os.environ['ENVIRONMENT'] = environment
        os.environ['AWS_ACCOUNT_ID'] = aws_account_id
        click.echo(f"Configuration saved: AWS account ID = {aws_account_id}, Environment = {environment}, Base Path = {base_path}, Branch = {branch}")