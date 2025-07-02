# 🧩 External Imports ────────────────────────────────────────────────
import click
from rich.console import Console
from datetime import datetime, UTC
from werkzeug.exceptions import NotFound

# 🏗️ Internal Imports ────────────────────────────────────────────────
from Epic_events.database import SessionLocal
from Epic_events.models import Client, User, Contract, UserRole
from Epic_events.rich_styles import build_table

# 🎨 Rich Console Setup ──────────────────────────────────────────────
console = Console()


# 🖼️ Utility: Render Contracts Table ─────────────────────────────────
def render_contracts_table(contracts, title: str):
    table = build_table(title, ["🆔 ID", "🤑 Total Amount", "💰 Remains to pay", "🤝 Is Signed",
                                        "👤 Commercial Ref", "💼 Client Ref"])
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


# 📝 Create Contract ─────────────────────────────────────────────────
def create_contract_logic():
    session = SessionLocal()
    now = datetime.now(UTC)

    try:
        amount_total = click.prompt("🤑 Total amount of the contract", type=float)
        amount_due = click.prompt("💰 Remains to pay", type=float)
        is_signed = click.prompt("✅ Is the contract signed? (True/False)", type=bool)
        commercial_id = click.prompt("🧑‍💼 Commercial ID", type=int)
        client_id = click.prompt("👤 Client ID", type=int)

        client = session.query(Client).filter_by(client_id=client_id).first()
        if not client:
            console.print(f"[red]❌ Client with ID {client_id} not found.[/red]")
            return

        user = session.query(User).filter_by(user_id=commercial_id).first()
        if not user:
            console.print(f"[red]❌ User with ID {commercial_id} not found.[/red]")
            return
        console.print(f"[yellow]Debug: user.role = {user.role}[/yellow]")

        if user.role != UserRole.commercial:
            console.print(f"[red]❌ User with ID {commercial_id} is not a commercial.[/red]")
            return

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


# 📋 List All Contracts ──────────────────────────────────────────────
def list_contracts_logic():
    """List All Contracts regardless of role."""
    session = SessionLocal()

    try:
        contracts = session.query(Contract).all()

        if not contracts:
            console.print("[yellow]⚠️ No Contracts found.[/yellow]")
            return
        render_contracts_table(contracts, title="📋 All Contracts")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

    finally:
        session.close()


# 📄 List Contracts for a Client ─────────────────────────────────────
def list_client_contracts_logic(client_id: int):
    """List contracts linked to a specific client."""
    session = SessionLocal()

    try:
        contracts = session.query(Contract).filter(Contract.client_id == client_id).all()

        if not contracts:
            console.print("[yellow]⚠️ No Contracts found.[/yellow]")
            return
        render_contracts_table(contracts, title=f"📋 Contracts for Client {client_id}")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

    finally:
        session.close()


# 🔧 Update Contract ─────────────────────────────────────────────────
def update_contract_logic(contract_id: int):
    session = SessionLocal()
    updated_fields = {}

    try:
        contract = session.query(Contract).filter(Contract.contract_id == contract_id).first()
        if not contract:
            raise NotFound(f"Contract with ID {contract_id} not found.")

        click.secho("📋 Leave any field blank to skip updating it.", fg="cyan")

        while True:
            amount_total = click.prompt("🤑 Total amount of the contract", default="", show_default=False)
            if amount_total == "":
                break
            if amount_total.isdigit():
                updated_fields["amount_total"] = amount_total
                click.secho("✅ Total amount updated.", fg="green")
                break
            else:
                click.secho("❌ Please enter digits only.", fg="red")

        while True:
            amount_due = click.prompt("💰 Remains to pay", default="", show_default=False)
            if amount_due == "":
                break
            if amount_due.isdigit():
                updated_fields["amount_due"] = amount_due
                click.secho("✅ Remaining amount updated.", fg="green")
                break
            else:
                click.secho("❌ Please enter digits only.", fg="red")

        while True:
            is_signed = click.prompt("✅ Is the contract signed? (True/False)", default="", show_default=False)
            if is_signed == "":
                break
            if is_signed.lower() in ["true", "false"]:
                updated_fields["is_signed"] = is_signed.lower()
                click.secho("✅ Contract signature status updated.", fg="green")
                break
            else:
                click.secho("❌ Please enter 'True' or 'False' only.", fg="red")

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


# 🔄 Reassign Contract ───────────────────────────────────────────────
def reassign_contract_logic(contract_id: int):
    session = SessionLocal()
    updated_fields = {}

    try:
        contract = session.query(Contract).filter(Contract.contract_id == contract_id).first()
        if not contract:
            raise NotFound(f"Contract with ID {contract_id} not found.")

        while True:
            new_commercial_id = click.prompt("👔 Enter the new commercial's user ID", default="", show_default=False)
            if new_commercial_id == "":
                break
            if new_commercial_id.isdigit():
                new_commercial_id = int(new_commercial_id)
                new_commercial = session.query(User).filter(
                    User.user_id == new_commercial_id, User.role == "commercial").first()
                if not new_commercial:
                    click.secho(f"❌ User ID {new_commercial_id} is not a valid commercial.", fg="red")
                    continue
                updated_fields["commercial_id"] = new_commercial_id
                click.secho("✅ New commercial assigned.", fg="green")
                break
            else:
                click.secho("❌ Please enter a valid integer.", fg="red")

        while True:
            new_client_id = click.prompt("👨🏻‍💼 Enter the new client ID", default="", show_default=False)
            if new_client_id == "":
                break
            if new_client_id.isdigit():
                new_client_id = int(new_client_id)
                new_client = session.query(Client).filter(Client.client_id == new_client_id).first()
                if not new_client:
                    click.secho(f"❌ Client ID {new_client_id} is not valid.", fg="red")
                    continue
                updated_fields["client_id"] = new_client_id
                click.secho(f"✅ Contract {contract_id} reassigned to new client.", fg="green")
                break
            else:
                click.secho("❌ Please enter a valid integer.", fg="red")

        if not updated_fields:
            click.secho("⚠️ No changes made to the contract.", fg="yellow")
            return

        if "commercial_id" in updated_fields:
            contract.commercial_id = updated_fields["commercial_id"]
        if "client_id" in updated_fields:
            contract.client_id = updated_fields["client_id"]

        session.commit()
        click.secho("✅ Contract updated successfully.", fg="green")

    except NotFound as nf:
        click.secho(str(nf), fg="red")
    except Exception as e:
        session.rollback()
        click.secho(f"❌ Unexpected error: {e}", fg="red")
    finally:
        session.close()


# 🗑️ Delete Contract ────────────────────────────────────────────────
def delete_contract_logic():
    session = SessionLocal()
    try:
        contract_id = click.prompt("🗑️ Enter the contract ID to delete", type=int)

        contract = session.query(Contract).filter(Contract.contract_id == contract_id).first()
        if not contract:
            raise NotFound(f"Contract with ID {contract_id} not found.")

        session.delete(contract)
        session.commit()
        click.secho(f"✅ Contract {contract_id} deleted successfully.", fg="green")

    except NotFound as nf:
        click.secho(str(nf), fg="red")
    except Exception as e:
        session.rollback()
        click.secho(f"❌ Unexpected error: {e}", fg="red")
    finally:
        session.close()
