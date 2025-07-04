"""
📄 Contract Command Handlers for Epic Events CRM

This module defines CLI commands for managing contracts: creation, updates, deletion, reassignment,
and listings. Permissions are enforced to ensure that only authorized roles can act on contracts.
"""

# 🥉 External Imports ──────────────────────────────────────────
import rich_click as click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# 🏗️ Internal Imports ──────────────────────────────────────────
from Epic_events.models import Contract
from Epic_events.auth.permissions import role_required, owner_required, attach_sentry_user
from Epic_events.service.contract_service import (
    create_contract_logic,
    list_contracts_logic,
    update_contract_logic,
    delete_contract_logic,
    list_client_contracts_logic,
    reassign_contract_logic,
    list_my_contracts_logic,
    list_contract_details_logic,
    list_not_signed_contract_logic,
)

console = Console()


# 🖼️ Utility for rendering command banners ───────────────────────────────
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


@click.group(
    cls=click.RichGroup,
    help="📋 Manage contracts: creation, update, deletion, and listing."
)
@click.pass_context
def contract(ctx):
    """📋 Contract Commands

    Group of commands for managing client contracts, including creation, updates,
    filtering by status or user, and deletions.
    """

    if ctx.invoked_subcommand:
        render_command_banner(
            "📋 Contract Command Group",
            "Manage contracts for client events, including creation,"
            "\nstatus updates, payment tracking, and assignments."
        )


# 📝 CLI Command: Create Contract ───────────────────────────
@contract.command(name="create")
@role_required(["gestion", "commercial"])
def create_contract():
    """📝 Create a new contract (gestion or commercial)."""
    render_command_banner("Create Contract", "Create and initialize a new event contract for a client.")
    create_contract_logic()


# 📋 CLI Commands: Contract Listings ───────────────────────────
@contract.command(name="list")
@role_required(["gestion", "commercial", "support"])
def list_contracts():
    """📋 List all contracts in the system (visible to all roles)."""
    render_command_banner("List Contracts", "View all contracts regardless of status or assignment.")
    list_contracts_logic()


# 📋 CLI Commands: Client Listings ───────────────────────────
@contract.command(name="list-my-contracts")
@role_required(["commercial"])
def list_my_contracts():
    """📋 List contracts assigned to the logged-in commercial user."""
    render_command_banner("My Contracts", "Display only the contracts assigned to your user account.")
    list_my_contracts_logic()


@contract.command(name="list-client-contracts")
@role_required(["gestion", "commercial", "support"])
def list_client_contracts():
    """📄 List contracts linked to a specific client."""
    render_command_banner("Client Contracts",
                          "Display all contracts associated with a selected client.")
    list_client_contracts_logic()


@contract.command(name="list-details")
@role_required(["gestion", "commercial", "support"])
def list_contract_details():
    """🔍 Show detailed information for a specific contract."""
    render_command_banner("Contract Details",
                          "Display full contract information.")
    list_contract_details_logic()


@contract.command(name="not-signed")
@role_required(["gestion", "commercial", "support"])
def list_not_signed():
    """❗ List all contracts that are not signed."""
    render_command_banner("Contract Details",
                          "Display full contract information.")
    list_not_signed_contract_logic()


# 🔧 CLI Command: Update Contract ────────────────────────────
@contract.command(name="update")
@click.option("--contract-id", type=int, prompt="🔹 Enter the Contract ID to update")
@attach_sentry_user
@owner_required(Contract, owner_field="commercial_id", id_arg="contract_id")
def update_contract(contract_id: int):
    """🔧 Update a contract's status or details (owner or gestion only)."""
    render_command_banner("Update Contract", "Modify the payment status or terms of an existing contract.")
    update_contract_logic(contract_id)


# 🔄 CLI Command: Reassign Contract ───────────────────────────
@contract.command(name="reassign")
@role_required(["gestion"])
def reassign_contract():
    """🔄 Reassign client or commercial for a contract (gestion only)."""
    render_command_banner("Reassign Contract", "Reassign the client or commercial contact tied to a contract.")
    contract_id = click.prompt("🔹 Enter contract ID", type=int)
    reassign_contract_logic(contract_id)


# 🗑️ CLI Command: Delete Contract ───────────────────────────
@contract.command(name="delete")
@role_required(["gestion"])
def delete_contract():
    """🗑️ Delete a contract by ID (gestion only)."""
    render_command_banner("Delete Contract", "Permanently remove a contract from the system by its ID.")
    delete_contract_logic()
