# 🧩 External Imports ────────────────────────────────────────────────
import click
from rich.console import Console
from datetime import datetime

from werkzeug.exceptions import NotFound

# 🏗️ Internal Imports ────────────────────────────────────────────────
from Epic_events.database import SessionLocal
from Epic_events.models import Client, User, Contract, Event
from Epic_events.rich_styles import build_table
from Epic_events.service.user_service import get_logged_in_user


# 🎨 Rich Console Setup ──────────────────────────────────────────────
console = Console()


# 🖼️ Utility: Render Events Table ───────────────────────────────────────────────
def render_events_table(events, title: str):
    """Render a styled Rich table of event entries with emoji-enhanced headers."""
    table = build_table(
        title,
        [
            "🆔 Event ID", "📝 Event Name", "📅 Start Date", "📅 End Date",
            "📍 Location", "👤 Support Ref", "💼 Client Ref", "📄 Contract Ref"
        ]
    )
    for event in events:
        table.add_row(
            str(event.event_id),
            str(event.event_name),
            str(event.start_date),
            str(event.end_date),
            str(event.location),
            str(event.support_id) if event.support_id else "❌ Unassigned",
            str(event.client_id) if event.client_id else "❌ Unassigned",
            str(event.contract_id),
        )
    console.print(table)


# 🧠 Utility: Prompt for a DateTime ─────────────────────────────────────────────
def prompt_for_date(label, required=True):
    """
    Prompt the user to input a datetime in format 'DD-MM-YYYY HH:MM'.

    Args:
        label (str): Descriptive label for the field (e.g., 'Start Date').
        required (bool): Whether the field is mandatory. If False, input can be skipped.

    Returns:
        datetime | None: Parsed datetime object or None if skipped.
    """
    while True:
        date_str = click.prompt(f"🗓️ {label} (format: DD-MM-YYYY HH:MM)", default="", show_default=False)

        if not date_str:
            if required:
                click.secho("❌ This field is required. Please enter a valid date.", fg="red")
                continue
            return None

        try:
            return datetime.strptime(date_str, "%d-%m-%Y %H:%M")
        except ValueError:
            click.secho("❌ Invalid date format. Please use 'DD-MM-YYYY HH:MM'.", fg="red")


# 📝 Create Contract ─────────────────────────────────────────────────
def create_event_logic():
    """📌 Create a new event and link it to a contract, client, and support user."""
    session = SessionLocal()
    user = get_logged_in_user()

    try:
        # 🔍 Validate Client
        while True:
            client_id = click.prompt("👤 Client ID", type=int)
            client = session.query(Client).filter_by(client_id=client_id).first()
            if not client:
                console.print(f"[red]❌ No client found with ID {client_id}. Try again.[/red]")
                continue

            # 🔒 Authorization check for commercial
            if user.role.value == "commercial" and client.commercial_id != user.user_id:
                click.secho(f"📋 Client is assigned to commercial ID: {client.commercial_id}", fg="yellow")
                click.secho(f"👤 Logged-in user ID: {user.user_id}", fg="yellow")
                return
            break

        event_name = click.prompt("📝 Enter the event name", type=str)
        start_date = prompt_for_date("📅 Event's Start Date")
        end_date = prompt_for_date("📅 Event's End Date")
        location = click.prompt("📍 Enter the event location", type=str)
        notes = click.prompt("🗒️ Notes or description", type=str)

        # 🔧 Validate Support Contact
        while True:
            support_id = click.prompt("👨‍🔧 Support ID", type=int)
            support = session.query(User).filter_by(user_id=support_id, role="support").first()
            if not support:
                console.print(f"[red]❌ No support user found with ID {support_id}. Try again.[/red]")
                continue
            break

        # 📄 Validate Contract
        while True:
            contract_id = click.prompt("📄 Contract ID", type=int)
            contract = session.query(Contract).filter_by(contract_id=contract_id).first()
            if not contract:
                console.print(f"[red]❌ No contract found with ID {contract_id}. Try again.[/red]")
                continue
            break

        # ✅ Create the Event
        event = Event(
            event_name=event_name,
            start_date=start_date,
            end_date=end_date,
            location=location,
            notes=notes,
            support_id=support_id,
            client_id=client_id,
            contract_id=contract_id,
        )
        session.add(event)
        session.commit()

        console.print(f"[green]✅ Event '{event.event_name}' successfully created and linked to contract "
                      f"{contract_id} for {client.full_name}.[/green]")

    except Exception as e:
        session.rollback()
        console.print(f"[red]❌ Error creating event: {e}[/red]")

    finally:
        session.close()


# 📋 List All Contracts ──────────────────────────────────────────────
def list_event_details_logic():
    """📋 Display details for a single event by ID."""
    session = SessionLocal()

    try:
        while True:
            event_id = click.prompt("🔎 Enter the Event ID to show details", type=int)
            event = session.query(Event).filter(Event.event_id == event_id).first()

            if not event:
                console.print(f"[yellow]⚠️ No event found with ID {event_id}. Please try again.[/yellow]")
                continue

            render_events_table([event], title=f"📋 Event {event_id} Details")
            return

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

    finally:
        session.close()


# 📋 List All Contracts ──────────────────────────────────────────────
def list_events_logic():
    """📋 List all events, regardless of user role."""
    session = SessionLocal()

    try:
        events = session.query(Event).all()

        if not events:
            console.print("[yellow]⚠️ No events found in the system.[/yellow]")
            return

        render_events_table(events, title="📋 All Events")

    except Exception as e:
        console.print(f"[red]❌ Error while listing events: {e}[/red]")

    finally:
        session.close()


# 📋 List My Events ─────────────────────────────────────────────────
def list_my_events_logic():
    """List clients assigned to the logged-in commercial user only."""
    user = get_logged_in_user()
    session = SessionLocal()

    try:
        events = session.query(Event).filter(Event.support_id == user.user_id).all()

        if not events:
            console.print("[yellow]⚠️ You have no clients assigned.[/yellow]")
            return

        render_events_table(events, title=f"📋 Event Assigned to {user.name}")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
    finally:
        session.close()


# 📄 List Contracts for a Client ─────────────────────────────────────
def list_client_events_logic():
    """📄 List all events linked to a specific client."""
    session = SessionLocal()

    try:
        while True:
            client_id = click.prompt("🔎 Enter the Client ID to list their events", type=int)
            events = session.query(Event).filter(Event.client_id == client_id).all()

            if not events:
                console.print(f"[yellow]⚠️ No events found for client ID {client_id}. Try another one.[/yellow]")
                continue

            render_events_table(events, title=f"📋 Events for Client {client_id}")
            return

    except Exception as e:
        console.print(f"[red]❌ Error while listing client events: {e}[/red]")

    finally:
        session.close()


# 🔧 Update Contract ─────────────────────────────────────────────────
def update_event_logic(event_id: int):
    """🔧 Update an event's details interactively via the CLI."""
    session = SessionLocal()
    updated_fields = {}

    try:
        # 🆔 Prompt for Event ID
        while True:
            event_id = click.prompt("✏️ Confirm the Event ID to update", type=int)
            event = session.query(Event).filter(Event.event_id == event_id).first()
            if not event:
                click.secho(f"❌ No event found with ID {event_id}. Please try again.", fg="red")
                continue

            click.secho(f"🔧 Updating event ID {event_id}...", fg="blue")
            click.secho("📋 Leave any field blank to skip updating it.", fg="cyan")
            break

        # 📝 Optional fields
        event_name = click.prompt("📝 New Event Name", default="", show_default=False)
        if event_name:
            updated_fields["event_name"] = event_name
            click.secho("✅ Event name updated.", fg="green")

        start_date = prompt_for_date("📅 New Start Date", required=False)
        if start_date:
            updated_fields["start_date"] = start_date
            click.secho("✅ Start date updated.", fg="green")

        end_date = prompt_for_date("📅 New End Date", required=False)
        if end_date:
            updated_fields["end_date"] = end_date
            click.secho("✅ End date updated.", fg="green")

        location = click.prompt("📍 New Location", default="", show_default=False)
        if location:
            updated_fields["location"] = location
            click.secho("✅ Location updated.", fg="green")

        notes = click.prompt("🗒️ New Notes", default="", show_default=False)
        if notes:
            updated_fields["notes"] = notes
            click.secho("✅ Notes updated.", fg="green")

        if not updated_fields:
            click.secho("⚠️ No changes entered. Nothing was updated.", fg="yellow")
            return

        # 🧠 Apply changes
        for field, value in updated_fields.items():
            if hasattr(event, field):
                setattr(event, field, value)

        session.commit()
        click.secho(f"✅ Event ID {event_id} updated successfully!", fg="green")

    except Exception as e:
        session.rollback()
        click.secho(f"❌ Error updating event: {e}", fg="red")

    finally:
        session.close()


# 🔄 Reassign Contract ───────────────────────────────────────────────
def reassign_event_logic():
    """🔄 Reassign the support contact or client for an existing event."""
    session = SessionLocal()
    updated_fields = {}

    try:
        # 🔍 Find the event
        event_id = click.prompt("🔢 Enter Event ID", type=int)
        event = session.query(Event).filter(Event.event_id == event_id).first()
        if not event:
            raise NotFound(f"❌ Event with ID {event_id} not found.")

        # 👤 Reassign support
        while True:
            new_support_id = click.prompt("👔 Enter the new Support's user ID", default="", show_default=False)
            if new_support_id == "":
                break
            if not new_support_id.isdigit():
                click.secho("❌ Please enter a valid integer.", fg="red")
                continue

            new_support = session.query(User).filter(
                User.user_id == int(new_support_id), User.role == "support"
            ).first()
            if not new_support:
                click.secho(f"❌ User ID {new_support_id} is not a valid support.", fg="red")
                continue

            updated_fields["support_id"] = int(new_support_id)
            click.secho("✅ New Support assigned.", fg="green")
            break

        # 🧑 Reassign client
        while True:
            new_client_id = click.prompt("👨🏻‍💼 Enter the new Client ID", default="", show_default=False)
            if new_client_id == "":
                break
            if not new_client_id.isdigit():
                click.secho("❌ Please enter a valid integer.", fg="red")
                continue

            new_client = session.query(Client).filter(Client.client_id == int(new_client_id)).first()
            if not new_client:
                click.secho(f"❌ Client ID {new_client_id} is not valid.", fg="red")
                continue

            updated_fields["client_id"] = int(new_client_id)
            click.secho(f"✅ Event '{event.event_name}' reassigned to new client.", fg="green")
            break

        # 🛑 No updates?
        if not updated_fields:
            click.secho("⚠️ No changes made to the event.", fg="yellow")
            return

        # 🧠 Apply updates
        if "support_id" in updated_fields:
            event.support_id = updated_fields["support_id"]
        if "client_id" in updated_fields:
            event.client_id = updated_fields["client_id"]

        session.commit()
        click.secho("✅ Event reassignment saved successfully.", fg="green")

    except NotFound as nf:
        click.secho(str(nf), fg="red")
    except Exception as e:
        session.rollback()
        click.secho(f"❌ Unexpected error: {e}", fg="red")
    finally:
        session.close()


# 🗑️ Delete Contract ────────────────────────────────────────────────
def delete_event_logic():
    """🗑️ Delete an event by its ID."""
    session = SessionLocal()
    try:
        event_id = click.prompt("🗑️ Enter the Event ID to delete", type=int)
        event = session.query(Event).filter(Event.event_id == event_id).first()

        if not event:
            raise NotFound(f"❌ Event with ID {event_id} not found.")

        session.delete(event)
        session.commit()
        click.secho(f"✅ Event ID {event_id} deleted successfully.", fg="green")

    except NotFound as nf:
        click.secho(str(nf), fg="red")
    except Exception as e:
        session.rollback()
        click.secho(f"❌ Unexpected error: {e}", fg="red")
    finally:
        session.close()
