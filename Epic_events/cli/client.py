# 🧩 External Imports ────────────────────────────────────────────────
import click

# 🏗️ Internal Imports ────────────────────────────────────────────────
from Epic_events.models import Client
from Epic_events.auth.permissions import role_required, owner_required
from Epic_events.service.client_service import (
    register_client_logic,
    list_clients_logic,
    list_my_clients_logic,
    delete_client_logic,
    update_client_logic,
    reassign_commercial_logic
)


# 📝 CLI Commands: Client Registration & Update ──────────────────────
@click.command()
@role_required(["commercial"])
def register_client():
    """📝 Register a new client (commercial only)."""
    click.secho("📝 Registering a new client...", fg="cyan")
    register_client_logic()


@click.command("update_client")
@click.option("--client-id", type=int, prompt="🔢 Enter the client ID to update")
@owner_required(Client, owner_field="commercial_id", id_arg="client_id")
def update_client(client_id):
    """
    🔧 Update a client's information (only if you are the assigned commercial or part of 'gestion').
    """
    click.secho(f"🔧 Updating client with ID {client_id}...", fg="cyan")
    update_client_logic(client_id)


# 🔄 CLI Command: Client Reassignment ─────────────────────────────────
@click.command("reassign_commercial")
@role_required(["gestion"])
def reassign_commercial():
    """
    🔄 Reassign a client to a different commercial (gestion only).
    """
    try:
        client_id = click.prompt("🔢 Enter the client ID to reassign", type=int)
        new_commercial_id = click.prompt("👔 Enter the new commercial's user ID", type=int)

        success_message = reassign_commercial_logic(client_id, new_commercial_id)
        click.secho(f"✅ {success_message}", fg="green")

    except ValueError as e:
        click.secho(f"❌ Error: {e}", fg="red")

    except Exception as e:
        click.secho(f"🚨 An unexpected error occurred: {e}", fg="red")


# 🗑️ CLI Command: Delete Client ───────────────────────────────────────
@click.command("delete-client")
@click.option("--client-id", type=int, prompt="🗑️ Enter the client ID to delete")
@owner_required(Client, owner_field="commercial_id", id_arg="client_id")
def delete_client(client_id):
    """
    🗑️ Delete a client by ID (if you are the owner or part of 'gestion team').
    """
    try:
        message = delete_client_logic(client_id)
        click.secho(f"✅ {message}", fg="green")
    except Exception as e:
        click.secho(f"❌ Error: {e}", fg="red")


# 📋 CLI Commands: Client Listings ────────────────────────────────────
@click.command()
@role_required(["commercial"])
def list_my_clients():
    """📋 List clients assigned to the logged-in commercial user only."""
    click.secho("📋 Listing your assigned clients...", fg="cyan")
    list_my_clients_logic()


@click.command()
@role_required(["commercial", "gestion", "support"])
def list_clients():
    """🌐 List all clients, regardless of role."""
    click.secho("🌐 Listing all clients in the system...", fg="cyan")
    list_clients_logic()
