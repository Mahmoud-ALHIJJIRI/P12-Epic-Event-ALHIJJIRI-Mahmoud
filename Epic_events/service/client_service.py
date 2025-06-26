import click
from rich.table import Table
from rich.console import Console
from sqlalchemy.orm import Session
from datetime import datetime, UTC

from Epic_events.database import SessionLocal
from Epic_events.models import Client
from Epic_events.auth.permissions import role_required
from Epic_events.service.user_service import get_logged_in_user


console = Console()


def render_clients_table(clients, title: str):
    table = Table(title=title)
    table.add_column("ID", justify="right")
    table.add_column("Full Name", style="bold")
    table.add_column("Email")
    table.add_column("Phone")
    table.add_column("Company")
    table.add_column("Assigned To")

    for client in clients:
        table.add_row(
            str(client.id),
            client.full_name,
            client.email,
            client.phone,
            client.company_name,
            str(client.commercial_id) if client.commercial_id else "Unassigned"
        )

    console.print(table)


def register_client_logic():
    """Register a new client (commercial only)."""
    session: Session = SessionLocal()
    try:
        # Get Logged_in user (commercial)
        user = get_logged_in_user()

        full_name = click.prompt("Client Full Name")
        email = click.prompt("Client email")
        phone = click.prompt("Client Phone")
        company_name = click.prompt("Company Name")

        now = datetime.now(UTC)

        client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            created_date=now,
            last_contact=now,
            commercial_id=user.id
        )

        session.add(client)
        session.commit()
        console.print(f"[green]✅ Client '{full_name}' added successfully![/green]")

    except Exception as e:
        session.rollback()
        console.print(f"[red]❌ Error creating client: {e}[/red]")

    finally:
        session.close()


def list_my_clients_logic():
    """List clients assigned to the logged-in commercial user only."""
    user = get_logged_in_user()
    session = SessionLocal()

    try:
        clients = session.query(Client).filter(Client.commercial_id == user.id).all()

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

