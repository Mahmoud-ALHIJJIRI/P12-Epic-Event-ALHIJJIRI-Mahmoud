# 🧩 External Imports ────────────────────────────────────────────────
import click

# 🏗️ Internal Imports ────────────────────────────────────────────────
from Epic_events.models import Contract
from Epic_events.auth.permissions import role_required, owner_required
from Epic_events.service.contract_service import (
    create_contract_logic,
    list_contracts_logic,
    update_contract_logic,
    delete_contract_logic,
    list_client_contracts_logic,
    reassign_contract_logic
)


# 📝 CLI Command: Create Contract ─────────────────────────────────────
@click.command()
@role_required(["gestion"])
def create_contract():
    """📝 Create a new contract (gestion only)."""
    create_contract_logic()


# 📋 CLI Commands: Contract Listings ──────────────────────────────────
@click.command()
@role_required(["gestion", "commercial", "support"])
def list_contracts():
    """📋 List all contracts in the system."""
    list_contracts_logic()


@click.command()
@role_required(["gestion", "commercial", "support"])
def list_client_contracts():
    """📄 List contracts linked to a specific client."""
    client = click.prompt("🔎 Enter Client ID to list attached contracts")
    list_client_contracts_logic(client)


# 🔧 CLI Command: Update Contract ─────────────────────────────────────
@click.command()
@click.option("--contract-id", type=int, prompt="🔢 Enter the contract ID to update")
@owner_required(Contract, owner_field="commercial_id", id_arg="contract_id")
def update_contract(contract_id):
    """
    🔧 Update a contract's information (only if you are the assigned commercial or part of 'gestion').
    """
    click.secho(f"🔧 Updating contract with ID {contract_id}...", fg="cyan")
    update_contract_logic(contract_id)


# 🔄 CLI Command: Reassign Contract ───────────────────────────────────
@click.command()
@role_required(["gestion"])
def reassign_contract():
    """🔄 Reassign a client or commercial to an existing contract (gestion only)."""
    contract_id = click.prompt("🔢 Enter contract ID", type=int)
    reassign_contract_logic(contract_id)


# 🗑️ CLI Command: Delete Contract ─────────────────────────────────────
@click.command("delete_contract")
@role_required(["gestion"])
def delete_contract():
    """🗑️ Delete a contract by ID (gestion only)."""
    delete_contract_logic()
