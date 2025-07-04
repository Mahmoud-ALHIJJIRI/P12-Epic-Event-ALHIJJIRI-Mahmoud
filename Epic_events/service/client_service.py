"""
👥 Client Business Logic Layer for Epic Events CRM

This module provides all backend logic for managing client data including creation,
updates, deletion, reassignment, and listing. It communicates with the database and
enforces validations before changes are made.
"""

# 🧩 External Imports ────────────────────────────────────────────────
import click
from rich.console import Console
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, UTC
from werkzeug.exceptions import NotFound

# 🏗️ Internal Imports ────────────────────────────────────────────────
from Epic_events.database import SessionLocal
from Epic_events.models import Client, User
from Epic_events.service.user_service import get_logged_in_user
from Epic_events.rich_styles import build_table

# 🎨 Rich Console Instance ─────────────────────────────────────────────
console = Console()


# 🖼️ Utility: Render a rich table of clients ─────────────────────────────
def render_clients_table(clients, title: str):
    table = build_table(title, ["👤 ID", "🧑 Full Name", "📧 Email", "🔐 phone", " 🏢 Company",
                                "👤 Commercial Ref", "Creation date", "Last Contact"])
    for client in clients:
        table.add_row(
            str(client.client_id),
            client.full_name,
            client.email,
            str(client.phone),
            client.company_name,
            str(client.commercial_id) if client.commercial_id else "Unassigned",
            str(client.created_date),
            str(client.last_contact)
        )
    console.print(table)


# 📝 Register a New Client ──────────────────────────────────────────────
def register_client_logic():
    """Register a new client (commercial only)."""
    session = SessionLocal()
    try:
        user = get_logged_in_user()

        full_name = click.prompt("👤 Client Full Name")
        while True:
            email = click.prompt("📧 Client Email")
            existing = session.query(Client).filter(Client.email == email).first()
            if existing:
                console.print(f"[red]❌ Email '{email}' already exists. Please enter a different one.[/red]")
            else:
                break

        phone = click.prompt("📱 Client Phone (digits only)", type=int)
        company_name = click.prompt("🏢 Company Name")
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


# 🔧 Update an Existing Client ─────────────────────────────────────────────
def update_client_logic(client_id: int):
    session = SessionLocal()
    now = datetime.now(UTC)
    updated_fields = {}
    try:
        client = session.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            raise NotFound(f"Client with ID {client_id} not found.")

        click.secho("📋 Leave any field blank to skip updating it.", fg="cyan")

        updated_fields["last_contact"] = now

        full_name = click.prompt("👤 Full Name", default="", show_default=False)
        if full_name:
            updated_fields["full_name"] = full_name
            click.secho("✅ Full Name updated.", fg="green")

        company_name = click.prompt("🏢 Company Name", default="", show_default=False)
        if company_name:
            updated_fields["company_name"] = company_name
            click.secho("✅ Company Name updated.", fg="green")

        while True:
            email = click.prompt("📧 Email (leave blank to skip)", default="", show_default=False)
            if not email:
                break
            existing = session.query(Client).filter(Client.email == email, Client.client_id != client_id).first()
            if existing:
                console.print(f"[red]❌ Email '{email}' "
                              f"already exists. Please enter a different one or leave blank.[/red]")
            else:
                updated_fields["email"] = email
                click.secho("✅ Email updated.", fg="green")
                break

        while True:
            phone = click.prompt("📱 Phone (leave blank to skip)", default="", show_default=False)
            if not phone:
                break

            if phone.isdigit():
                updated_fields["phone"] = phone
                click.secho("✅ Phone number updated.", fg="green")
                break
            else:
                click.secho("❌ Error: Phone number must contain only digits.", fg="red")

        if not updated_fields:
            click.secho("⚠️ No changes entered. Nothing to update.", fg="yellow")
            return

        for field, value in updated_fields.items():
            if hasattr(client, field):
                setattr(client, field, value)

        session.commit()
        click.secho(f"✅ Client with ID {client_id} has been updated.", fg="green")

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


# 🔄 Reassign Commercial to Client ─────────────────────────────────────
def reassign_commercial_logic(client_id: int, new_commercial_id: int):
    session = SessionLocal()
    try:
        client = session.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            raise NotFound(f"Client with ID {client_id} not found.")

        new_commercial = session.query(User).filter(
            User.user_id == new_commercial_id, User.role == "commercial").first()
        if not new_commercial:
            raise NotFound(f"User ID {new_commercial_id} is not a valid commercial.")

        client.commercial_id = new_commercial_id
        session.commit()
        return f"✅  Client {client_id} is now assigned to commercial {new_commercial_id}."

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


# 🗑️ Delete a Client ─────────────────────────────────────────────────────
def delete_client_logic(client_id: int):
    session = SessionLocal()
    try:
        client = session.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            raise NotFound(f"Client with ID {client_id} not found.")

        session.delete(client)
        session.commit()
        return f"✅ Client with ID {client_id} has been deleted."

    except IntegrityError as ie:
        session.rollback()
        console.print(f"[yellow]❌ Foreign key error: {ie.orig}[/yellow]")

    except Exception as e:
        session.rollback()
        raise Exception(f"Unexpected error: {e}")
    finally:
        session.close()


# 📋 List Clients Assigned to Logged-in Commercial ────────────────────────
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


# 🌐 List All Clients ───────────────────────────────────────────────────────
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


# 🔍 Display Details for a Specific Client ───────────────────────────────
def list_client_details_logic():
    """📋 Display details for a single event by ID."""
    session = SessionLocal()

    try:
        while True:
            client_id = click.prompt("🔎 Enter the Client ID to show details", type=int)
            client = session.query(Client).filter(Client.client_id == client_id).first()

            if not client:
                console.print(f"[yellow]⚠️ No client found with ID {client_id}. Please try again.[/yellow]")
                continue

            render_clients_table([client], title=f"📋 Event {client_id} Details")
            return

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

    finally:
        session.close()
