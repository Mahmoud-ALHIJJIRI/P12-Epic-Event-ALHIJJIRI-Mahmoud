import click
from .user import register_user, login, whoami, list_users
from .client import register_client, list_clients, list_my_clients


@click.group()
def cli():
    """Epic Events CLI"""
    pass


# Register subcommands to CLI (users)
cli.add_command(register_user, name="register_user")
cli.add_command(login, name="login")
cli.add_command(whoami, name="whoami")
cli.add_command(list_users, name="list_users")

# Register subcommands to CLI (clients)
cli.add_command(register_client, name="register_client")
cli.add_command(list_clients, name="list_clients")
cli.add_command(list_my_clients, name="list_my_clients")
