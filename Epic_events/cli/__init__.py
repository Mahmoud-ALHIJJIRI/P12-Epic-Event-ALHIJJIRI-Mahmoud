import click
from .user import register_user, login, whoami


@click.group()
def cli():
    """Epic Events CLI"""
    pass


# Register subcommands to CLI group
cli.add_command(register_user, name="register-user")
cli.add_command(login, name="login")
cli.add_command(whoami, name="whoami")
