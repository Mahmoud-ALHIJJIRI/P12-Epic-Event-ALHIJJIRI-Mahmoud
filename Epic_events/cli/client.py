# 🥉 External Imports ──────────────────────────────────────────
import rich_click as click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# 🏗️ Internal Imports ──────────────────────────────────────────
from Epic_events.models import Client
from Epic_events.auth.permissions import role_required, owner_required
from Epic_events.service.client_service import (
    register_client_logic,
    list_clients_logic,
    list_my_clients_logic,
    delete_client_logic,
    update_client_logic,
    reassign_commercial_logic,
    list_client_details_logic,
)

console = Console()

# 🔹 Reusable Banner Function ──────────────────────────────


def render_command_banner(title: str, message: str):
    banner = Panel(
        Text(message, justify="left", style="bold yellow"),
        title=f"[bold magenta]{title}[/bold magenta]",
        subtitle="[italic cyan]Your Command-Line CRM[/italic cyan]",
        border_style="green",
        padding=(1, 2),
        expand=False
    )
    console.print(Align.left(banner))


# ─── 👥 Client Command Group ──────────────────────────────
@click.group(
    cls=click.RichGroup,
    help="👥 Manage client accounts, contact info, and linked contracts."
)
@click.pass_context
def client(ctx):
    """👥 Client Commands"""

    if ctx.invoked_subcommand:
        render_command_banner(
            "👥 Client Command Group",
            "Register, update, and view client profiles.\nLink clients to contracts and scheduled events."
        )


# 📝 CLI Commands: Client Registration & Update ──────────────────────────
@client.command(name="register")
@role_required(["commercial"])
def register_client():
    """📝 Register a new client (commercial only)."""
    render_command_banner("Register Client", "Register a new client profile and assign a commercial contact.")
    register_client_logic()


@client.command("update")
@click.option("--client-id", type=int, prompt="🔹 Enter the client ID to update")
@owner_required(Client, owner_field="commercial_id", id_arg="client_id")
def update_client(client_id):
    """🔧 Update a client's information (only if you are the assigned commercial or part of 'gestion')."""
    render_command_banner("Update Client", "Update a client's contact information or business name.")
    update_client_logic(client_id)


# 🔄 CLI Command: Client Reassignment ────────────────────────────
@client.command("reassign")
@role_required(["gestion"])
def reassign_commercial():
    """🔄 Reassign a client to a different commercial (gestion only)."""
    render_command_banner("Reassign Commercial", "Assign a different commercial to an existing client.")
    try:
        client_id = click.prompt("🔹 Enter the client ID to reassign", type=int)
        new_commercial_id = click.prompt("💼 Enter the new commercial's user ID", type=int)

        success_message = reassign_commercial_logic(client_id, new_commercial_id)
        click.secho(f" {success_message}", fg="green")

    except ValueError as e:
        click.secho(f"❌ Error: {e}", fg="red")

    except Exception as e:
        click.secho(f"🚨 An unexpected error occurred: {e}", fg="red")


# 🗑️ CLI Command: Delete Client ────────────────────────────
@client.command("delete")
@click.option("--client-id", type=int, prompt="🗑️ Enter the client ID to delete")
@owner_required(Client, owner_field="commercial_id", id_arg="client_id")
def delete_client(client_id):
    """🗑️ Delete a client by ID (if you are the owner or part of 'gestion team')."""
    render_command_banner("Delete Client", "Permanently remove a client profile from the system.")
    try:
        message = delete_client_logic(client_id)
        click.secho(f"✅ {message}", fg="green")
    except Exception as e:
        click.secho(f"❌ Error: {e}", fg="red")


# 📋 CLI Commands: Client Listings ───────────────────────────
@client.command(name="list-my-clients")
@role_required(["commercial"])
def list_my_clients():
    """📋 List clients assigned to the logged-in commercial user only."""
    render_command_banner("My Clients", "Display only the clients assigned to your user account.")
    list_my_clients_logic()


@client.command(name="list-clients")
@role_required(["commercial", "gestion", "support"])
def list_clients():
    """🌐 List all clients, regardless of role."""
    render_command_banner("All Clients", "View all client records in the system.")
    list_clients_logic()


@client.command(name="list-details")
@role_required(["gestion", "commercial", "support"])
def list_client_details():
    """🔍 Show detailed information for a specific client."""
    render_command_banner("Client Details",
                          "Display full client information.")
    list_client_details_logic()
