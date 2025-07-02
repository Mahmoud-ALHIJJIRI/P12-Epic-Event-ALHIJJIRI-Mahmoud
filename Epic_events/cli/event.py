# 🧩 External Imports ────────────────────────────────────────────────
import click

# 🏗️ Internal Imports ────────────────────────────────────────────────
from Epic_events.models import Contract
from Epic_events.auth.permissions import role_required, owner_required
from Epic_events.service.event_service import (
    create_event_logic,
    list_event_details_logic,
    list_events_logic,
    update_event_logic,
    delete_event_logic,
    list_client_events_logic,
    reassign_event_logic
)


# 📝 CLI Command: Create Contract ─────────────────────────────────────
@click.command()
@role_required(["gestion"])
def create_event():
    """📝 Create a new contract (gestion only)."""
    create_event_logic()


@click.command()
@role_required(["gestion", "commercial", "support"])
def list_event_details():
    list_event_details_logic()


# 📋 CLI Commands: Contract Listings ──────────────────────────────────
@click.command()
@role_required(["gestion", "commercial", "support"])
def list_events():
    """📋 List all contracts in the system."""
    list_events_logic()


@click.command()
@role_required(["gestion", "commercial", "support"])
def list_client_events():
    """📄 List contracts linked to a specific client."""
    list_client_events_logic()


# 🔧 CLI Command: Update Contract ─────────────────────────────────────
@click.command()
@owner_required(Contract, owner_field="support_id", id_arg="contract_id")
def update_event():
    """
    🔧 Update a contract's information (only if you are the assigned commercial or part of 'gestion').
    """
    update_event_logic()


# 🔄 CLI Command: Reassign Contract ───────────────────────────────────
@click.command()
@role_required(["gestion"])
def reassign_event():
    """🔄 Reassign a client or support to an existing contract (gestion only)."""
    reassign_event_logic()


# 🗑️ CLI Command: Delete Contract ─────────────────────────────────────
@click.command("delete_contract")
@role_required(["gestion"])
def delete_event():
    """🗑️ Delete a contract by ID (gestion only)."""
    delete_event_logic()
