import click


from Epic_events.auth.permissions import role_required
from Epic_events.service.client_service import (register_client_logic, list_clients_logic,
                                                list_my_clients_logic)


@click.command()
@role_required(["commercial", "gestion"])
def register_client():
    """Register a new client (commercial only)."""
    register_client_logic()


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
