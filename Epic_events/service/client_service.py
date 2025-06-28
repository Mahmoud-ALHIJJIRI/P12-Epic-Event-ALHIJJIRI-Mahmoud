import click
from rich.console import Console
from sqlalchemy.orm import Session
from datetime import datetime, UTC

from werkzeug.exceptions import NotFound

from Epic_events.database import SessionLocal
from Epic_events.models import Client
from Epic_events.service.user_service import get_logged_in_user
from Epic_events.rich_styles import build_table

console = Console()


def render_clients_table(clients, title: str):

    table = build_table(title, ["👤 ID", "🧑 Full Name", "📧 Email", "🔐 phone",
                                        " 🏢 Company", "👤 Commercial Ref"])
    for client in clients:
        table.add_row(
            str(client.client_id),
            client.full_name,
            client.email,
            client.phone,
            client.company_name,
            str(client.commercial_id) if client.commercial_id else "Unassigned"
        )

    console.print(table)


def register_client_logic():
    """Register a new client (commercial only)."""
    session = SessionLocal()
    try:
        # Get Logged_in user (commercial)
        user = get_logged_in_user()

        full_name = click.prompt("👤Client Full Name")
        while True:
            email = click.prompt("📧 Client email")
            existing = session.query(Client).filter(Client.email == email).first()
            if existing:
                console.print(f"[red]❌ Email '{email}' already exists. Please enter a different one.[/red]")
            else:
                break
        phone = click.prompt("Client Phone (digits only)", type=int)
        company_name = click.prompt("Company Name")

        now = datetime.now(UTC)

        client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            created_date=now,
            last_contact=now,
            commercial_id=user.user_id
        )

        session.add(client)
        session.commit()
        console.print(f"[green]✅ Client '{full_name}' added successfully![/green]")

    except Exception as e:
        session.rollback()
        console.print(f"[red]❌ Error creating client: {e}[/red]")

    finally:
        session.close()


def update_client_logic(client_id: int):
    session = SessionLocal()
    updated_fields = {}
    try:
        client = session.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            raise NotFound(f"Client with ID {client_id} not found.")

        click.echo("📋 Leave any field blank to skip updating it.")

        full_name = click.prompt("👤 Full name", default="", show_default=False)

        if full_name:
            updated_fields["full_name"] = full_name
            click.echo("Client's Full Name has been updated")

        company_name = click.prompt("🏢 Company name", default="", show_default=False)

        if company_name:
            updated_fields["company_name"] = company_name
            click.echo("Client's Company Name has been updated")

        while True:
            email = click.prompt("📧 Email (leave blank to skip)", default="", show_default=False)
            if not email:
                break
            existing = session.query(Client).filter(Client.email == email, Client.client_id != client_id).first()

            if existing:
                console.print(
                    f"[red]❌ Email '{email}' already exists. Please enter a different one or leave blank.[/red]")
            else:
                updated_fields["email"] = email
                click.echo("Client's Email has been updated")
                break

        while True:
            phone = click.prompt("📱 Phone (leave blank to skip)", default="", show_default=False)
            if not phone:
                break

            if phone:
                if phone.isdigit():
                    click.echo("✅ Phone number accepted.")
                    updated_fields["phone"] = phone
                    click.echo("Client's Phone has been updated")
                    break

                else:
                    click.echo("❌ Error: Phone number must contain only digits.")

        if not updated_fields:
            click.echo("⚠️ No changes entered. Nothing to update.")
            return

        # ✅ Apply updates
        for field, value in updated_fields.items():
            if hasattr(client, field):
                setattr(client, field, value)

        session.commit()
        return f"✅ Client with ID {client_id} has been updated."

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_client_logic(client_id: int):
    session = SessionLocal()
    try:
        # Fetch the client
        client = session.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            raise NotFound(f"Client with ID {client_id} not found.")

        session.delete(client)
        session.commit()
        return f"✅ Client with ID {client_id} has been deleted."

    except Exception as e:
        session.rollback()
        raise Exception(f"Unexpected error: {e}")
    finally:
        session.close()


def list_my_clients_logic():
    """List clients assigned to the logged-in commercial user only."""
    user = get_logged_in_user()
    session = SessionLocal()

    try:
        clients = session.query(Client).filter(Client.commercial_id == user.user_id).all()

        if not clients:
            console.print("[yellow]⚠️ You have no clients assigned.[/yellow]")
            return

        render_clients_table(clients, title=f"📋 Clients Assigned to {user.name}")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
    finally:
        session.close()


def list_clients_logic():
    """List all clients, regardless of role."""
    get_logged_in_user()
    session: Session = SessionLocal()

    try:
        clients = session.query(Client).all()

        if not clients:
            console.print("[yellow]⚠️ No clients found.[/yellow]")
            return

        render_clients_table(clients, title="📋 All Clients")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
    finally:
        session.close()
