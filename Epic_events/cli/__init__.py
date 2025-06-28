import click
from .user import (register_admin, register_user, login, whoami, list_users, logout,
                   delete_user, update_user_role)
from .client import register_client, list_clients, list_my_clients, delete_client, update_client


@click.group()
def cli():
    """Epic Events CLI"""
    pass


# Register subcommands to CLI (users)
cli.add_command(register_admin, name="register_admin")
cli.add_command(register_user, name="register_user")
cli.add_command(login, name="login")
cli.add_command(whoami, name="whoami")
cli.add_command(list_users, name="list_users")
cli.add_command(logout, name="logout")
cli.add_command(delete_user, name="delete_user")
cli.add_command(update_user_role, name="update_user_role")

# Register subcommands to CLI (clients)
cli.add_command(register_client, name="register_client")
cli.add_command(list_clients, name="list_clients")
cli.add_command(list_my_clients, name="list_my_clients")
cli.add_command(delete_client, name="delete_client")
cli.add_command(update_client, name="update_client")
