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
    list_client_contracts_logic
)


@click.command()
@role_required(["gestion"])
def create_contract():
    create_contract_logic()


@click.command()
@role_required(["gestion", "commercial", "support"])
def list_contracts():
    list_contracts_logic()


@click.command()
@role_required(["gestion", "commercial", "support"])
def list_client_contracts():
    client = click.prompt("Enter Client Id to in order to list attached contracts")
    list_client_contracts_logic(client)


@click.command()
@click.option("--contract-id", type=int, prompt="🔢 Enter the contract ID to update")
@owner_required(Contract, owner_field="commercial_id", id_arg="contract_id")
def update_contract(contract_id):
    """
    🔧 Update a contract's information (only if you are the assigned commercial or part of 'gestion').
    """
    click.secho(f"🔧 Updating contract with ID {contract_id}...", fg="cyan")
    update_contract_logic(contract_id)


def delete_contract():
    pass
