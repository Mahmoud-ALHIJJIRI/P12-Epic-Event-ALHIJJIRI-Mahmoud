import click

from Epic_events.models import Client
from Epic_events.auth.permissions import role_required, owner_required
from Epic_events.service.client_service import (register_client_logic, list_clients_logic,
                                                list_my_clients_logic, delete_client_logic,
                                                update_client_logic)


@click.command()
@role_required(["commercial"])
def register_client():
    """Register a new client (commercial only)."""
    register_client_logic()


@click.command("update-client")
@click.option("--client-id", type=int, prompt="🔢 Enter the client ID to delete")
@owner_required(Client, owner_field="commercial_id", id_arg="client_id")
def update_client(client_id):
    """
    Update a client's information (only if you are the assigned commercial or part of 'gestion').
    """
    update_client_logic(client_id)


@click.command("delete-client")
@click.option("--client-id", type=int, prompt="🔢 Enter the client ID to delete")
@owner_required(Client, owner_field="commercial_id", id_arg="client_id")
def delete_client(client_id):
    """
    Delete a client by ID (if you are the owner or part of 'gestion team').
    """
    try:
        message = delete_client_logic(client_id)
        click.echo(message)
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@click.command()
@role_required(["commercial"])
def list_my_clients():
    """List clients assigned to the logged-in commercial user only."""
    list_my_clients_logic()


@click.command()
@role_required(["commercial", "gestion", "support"])
def list_clients():
    """List all clients, regardless of role."""
    list_clients_logic()
