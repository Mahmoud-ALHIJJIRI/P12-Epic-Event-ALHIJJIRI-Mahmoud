"""
🎉 Event Command Handlers for Epic Events CRM

This module defines CLI commands for managing client events, including creation, updates, reassignment,
deletion, and detailed views. Permissions are enforced based on role or ownership.
"""

# 🥉 External Imports ──────────────────────────────────────────
import rich_click as click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# 🏗️ Internal Imports ──────────────────────────────────────────
from Epic_events.models import Event, Contract
from Epic_events.auth.permissions import role_required, owner_required
from Epic_events.service.event_service import (
    create_event_logic,
    list_event_details_logic,
    list_events_logic,
    update_event_logic,
    delete_event_logic,
    list_client_events_logic,
    list_my_events_logic,
    reassign_event_logic
)

console = Console()


# 🖼️ Utility for rendering rich command banners ───────────────────────────
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


# ─── 🎉 Event Command Group ───────────────────────────────
@click.group(
    name="event",
    cls=click.RichGroup,
    help="🎉 Manage client events: planning, assignments, and updates."
)
@click.pass_context
def event(ctx):
    """🎉 Event Commands

    Command group for planning, updating, assigning, and tracking events related to signed client contracts.
    """

    if ctx.invoked_subcommand:
        render_command_banner(
            "🎉 Event Command Group",
            "Create, update, reassign, and track events organized\nfor your clients under signed contracts."
        )


# ─── 📝 Event Creation ──────────────────────────────
@event.command(name="create")
@role_required(["gestion", "commercial"])
def create():
    """📝 Create a new event (gestion or commercial)."""
    render_command_banner("Create Event", "Create a new event for a client with a signed contract.")
    create_event_logic()


# ─── 📋 Event Listings ──────────────────────────────
@event.command(name="list")
@role_required(["gestion", "commercial", "support"])
def list_events():
    """📋 List all events in the system (all roles)."""
    render_command_banner("List Events", "View all scheduled events across all departments.")
    list_events_logic()


# 📋 CLI Commands: Client Listings ───────────────────────────
@event.command(name="list-my-event")
@role_required(["support"])
def list_my_events():
    """📋 List events assigned to the logged-in support user."""
    render_command_banner("My Events",
                          "Display only the Events assigned to your user account.")
    list_my_events_logic()


@event.command(name="list-client")
@role_required(["gestion", "commercial", "support"])
def list_client_events():
    """📄 List all events associated with a specific client."""
    render_command_banner("List Client Events", "View all events associated with a selected client.")
    list_client_events_logic()


@event.command(name="list-details")
@role_required(["gestion", "commercial", "support"])
def list_event_details():
    """🔍 Show detailed information for a specific event."""
    render_command_banner("Event Details", "Display full event information including date, location, and contacts.")
    list_event_details_logic()


# ─── 🔧 Event Modification ──────────────────────────────
@event.command(name="update")
@click.option("--event-id", type=int, prompt="🔹 Enter the Event ID to update")
@owner_required(Event, owner_field="support_id", id_arg="event_id")
def update_event(event_id):
    """🔧 Update event details (support or gestion only)."""
    render_command_banner("Update Event", "Modify event details like location, time, and assigned staff.")
    update_event_logic(event_id)


@event.command(name="reassign")
@role_required(["gestion"])
def reassign_event():
    """🔄 Reassign support or client for an event (gestion only)."""
    render_command_banner("Reassign Event", "Reassign the support contact or client attached to an event.")
    reassign_event_logic()


# ─── 🗑️ Event Deletion ──────────────────────────────
@event.command(name="delete")
@role_required(["gestion"])
def delete_event():
    """🗑️ Delete an event by ID (gestion only)."""
    render_command_banner("Delete Event", "Permanently remove an event from the system by its ID.")
    delete_event_logic()
