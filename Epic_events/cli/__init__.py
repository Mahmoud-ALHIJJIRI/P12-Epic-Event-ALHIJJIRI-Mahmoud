# ─── External Imports ───────────────────────────────────────────────
import click

# ─── Internal Imports ───────────────────────────────────────────────
from .user import (
    register_admin,
    register_user,
    login,
    whoami,
    list_users,
    logout,
    delete_user,
    update_user_role
)

from .client import (
    register_client,
    list_clients,
    list_my_clients,
    delete_client,
    update_client,
    reassign_commercial
)

from .contract import (
    create_contract,
    list_contracts,
    update_contract,
    reassign_contract,
    delete_contract,
    list_client_contracts
)

from .event import (
    create_event,
    list_event_details,
    list_events,
    update_event,
    reassign_event,
    delete_event,
    list_client_events
)


# 🚀 ROOT CLI COMMAND GROUP ──────────────────────────────────────────
@click.group()
def cli():
    """\n📦 [bold blue]Epic Events CLI[/bold blue]\n
    Welcome to the Epic Events CRM command-line interface.\n
    Use the commands below to manage users, clients, and events.\n"""
    click.secho("🚀 Launching Epic Events CLI...", fg='green', bold=True)
    click.secho("Type --help after any command for more info.\n", fg='yellow')


# 👤 USER COMMANDS ───────────────────────────────────────────────────
cli.add_command(register_admin, name="register_admin")
cli.add_command(register_user, name="register_user")
cli.add_command(login, name="login")
cli.add_command(whoami, name="whoami")
cli.add_command(list_users, name="list_users")
cli.add_command(logout, name="logout")
cli.add_command(delete_user, name="delete_user")
cli.add_command(update_user_role, name="update_user_role")


# 🧑‍💼 CLIENT COMMANDS ───────────────────────────────────────────────
cli.add_command(register_client, name="register_client")
cli.add_command(list_clients, name="list_clients")
cli.add_command(list_my_clients, name="list_my_clients")
cli.add_command(delete_client, name="delete_client")
cli.add_command(update_client, name="update_client")
cli.add_command(reassign_commercial, name="reassign_commercial")


# 📋 CONTRACT COMMANDS ───────────────────────────────────────────────
cli.add_command(create_contract, name="create_contract")
cli.add_command(list_contracts, name="list_contracts")
cli.add_command(list_client_contracts, name="list_client_contracts")
cli.add_command(update_contract, name="update_contract")
cli.add_command(reassign_contract, name="reassign_contract")
cli.add_command(delete_contract, name="delete_contract")


# 📋 Event COMMANDS ───────────────────────────────────────────────
cli.add_command(create_event, name="create_event")
cli.add_command(list_event_details, name="list_event_details")
cli.add_command(list_events, name="list_events")
cli.add_command(list_client_events, name="list_client_events")
cli.add_command(update_event, name="update_event")
cli.add_command(reassign_event, name="reassign_event")
cli.add_command(delete_event, name="delete_event")
