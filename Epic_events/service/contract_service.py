# 🧩 External Imports ────────────────────────────────────────────────
import click
from rich.console import Console
from rich.table import Column
from sqlalchemy.orm import Session
from datetime import datetime, UTC
from werkzeug.exceptions import NotFound

# 🏗️ Internal Imports ────────────────────────────────────────────────
from Epic_events.database import SessionLocal
from Epic_events.models import Client, User, Contract, UserRole
from Epic_events.service.user_service import get_logged_in_user
from Epic_events.rich_styles import build_table

# 🎨 Rich Console Setup ──────────────────────────────────────────────
console = Console()


# 🖼️ Utility: Render Client Table ────────────────────────────────────
def render_contracts_table(contracts, title: str):
    table = build_table(title, ["🆔 ID", "🤑 Total Amount", "💰 Remains to pay", "🤝 Is Signed",
                                        " 👤 Commercial Ref", "💼 Client Ref"])
    for contract in contracts:
        table.add_row(
            str(contract.client_id),
            str(contract.contract_id),
            str(contract.amount_total),
            str(contract.amount_due),
            str(contract.is_signed),
            str(contract.commercial_id) if contract.commercial_id else "Unassigned",
            str(contract.client_id) if contract.commercial_id else "Unassigned"
        )
    console.print(table)


def create_contract_logic():
    session = SessionLocal()
    now = datetime.now(UTC)

    try:
        # 🧾 Prompt user inputs
        amount_total = click.prompt("🤑 Total amount of the contract", type=float)
        amount_due = click.prompt("💰 Remains to pay", type=float)
        is_signed = click.prompt("✅ Is the contract signed? (True/False)", type=bool)
        commercial_id = click.prompt("🧑‍💼 Commercial ID", type=int)
        client_id = click.prompt("👤 Client ID", type=int)

        # ✅ Check if client exists
        client = session.query(Client).filter_by(client_id=client_id).first()
        if not client:
            console.print(f"[red]❌ Client with ID {client_id} not found.[/red]")
            return

        # ✅ Check if user exists and is a commercial
        user = session.query(User).filter_by(user_id=commercial_id).first()
        if not user:
            console.print(f"[red]❌ User with ID {commercial_id} not found.[/red]")
            return
        console.print(f"[yellow]Debug: user.role = {user.role}[/yellow]")

        if user.role != UserRole.commercial:
            console.print(f"[red]❌ User with ID {commercial_id} is not a commercial.[/red]")
            return

        # ✅ Create the contract
        contract = Contract(
            amount_total=amount_total,
            amount_due=amount_due,
            created_at=now,
            is_signed=is_signed,
            commercial_id=commercial_id,
            client_id=client_id,
        )
        session.add(contract)
        session.commit()

        console.print(f"[green]✅ Contract ID '{contract.contract_id}' attached to client '{client_id}' "
                      f"added successfully![/green]")

    except Exception as e:
        session.rollback()
        console.print(f"[red]❌ Error creating contract: {e}[/red]")

    finally:
        session.close()


def list_contracts_logic():
    """List All Contracts regardless of role."""
    session = SessionLocal()

    try:
        contracts = session.query(Contract).all()

        if not contracts:
            console.print("[yellow]⚠️ No Contracts found.[/yellow]")
            return
        render_contracts_table(contracts, title="📋 All Clients")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

    finally:
        session.close()


def list_client_contracts_logic(client_id: int):
    """List All Contracts regardless of role."""
    session = SessionLocal()

    try:
        contracts = session.query(Contract).filter(Contract.client_id == client_id).all()

        if not contracts:
            console.print("[yellow]⚠️ No Contracts found.[/yellow]")
            return
        render_contracts_table(contracts, title="📋 All Clients")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

    finally:
        session.close()


def update_contract_logic(contract_id: int):
    session = SessionLocal()
    updated_fields = {}
    try:
        contract = session.query(Contract).filter(Contract.contract_id == contract_id)
        if not contract:
            raise NotFound(f"Contract with ID {contract_id} not found.")

        click.secho("📋 Leave any field blank to skip updating it.", fg="cyan")
        # 🧾 Prompt user inputs
        while True:
            amount_total = click.prompt("🤑 Total amount of the contract", default="", show_default=False)
            if amount_total.isdigit():
                updated_fields["amount_total"] = amount_total
                click.secho("✅ The remain amount has been updated.", fg="green")
                break
            else:
                click.secho("❌ The Total amount of the contract has been updated.", fg="red")

        while True:
            amount_due = click.prompt("💰 Remains to pay", default="", show_default=False)
            if amount_due.isdigit():
                updated_fields["amount_due"] = amount_due
                click.secho("✅ The remain amount has been updated.", fg="green")
                break
            else:
                click.secho("❌ The remain amount of the contract has been updated.", fg="red")

        is_signed = click.prompt("✅ Is the contract signed? (True/False)", type=bool,
                                 default="", show_default=False)
        commercial_id = click.prompt("🧑‍💼 Commercial ID", type=int,
                                     default="", show_default=False)
        client_id = click.prompt("👤 Client ID", type=int,
                                 default="", show_default=False)

        if amount_due:
            updated_fields["amount_due"] = amount_due

        if is_signed:
            updated_fields["is_signed"] = is_signed

        if commercial_id:
            updated_fields["commercial_id"] = commercial_id

        if client_id:
            updated_fields["client_id"] = client_id

        if not updated_fields:
            click.secho("⚠️ No changes entered. Nothing to update.", fg="yellow")
            return

        for field, value in updated_fields.items():
            if hasattr(contract, field):
                setattr(contract, field, value)

        session.commit()
        click.secho(f"✅ Contract with ID {contract_id} has been updated.", fg="green")

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_contract_logic():
    pass
