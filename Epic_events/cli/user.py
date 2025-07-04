"""
👤 User Command Handlers for Epic Events CRM

This module provides CLI commands to manage users, including authentication, registration,
role updates, deletions, and user information display. Access control and Sentry tracking
are integrated to ensure secure operations.
"""

# 🥉 External Imports ──────────────────────────────────────────
import rich_click as click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# 🏗️ Internal Imports ──────────────────────────────────────────
from Epic_events.auth.permissions import role_required, attach_sentry_user
from Epic_events.service.user_service import (
    register_user_logic,
    login_user,
    logout_user,
    get_logged_user_info,
    list_users_logic,
    delete_user_by_id,
    update_user_role_logic,
    list_user_details_logic,
)

console = Console()


# 🖼️ Utility for rendering rich CLI banners ─────────────────────────────
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


# ─── 👤 User Command Group ──────────────────────────────
@click.group(
    cls=click.RichGroup,
    help="👤 Manage users: creation, login, updates, and roles."
)
@click.pass_context
def user(ctx):
    """👤 User Commands

    Command group for managing user accounts: login, registration, role updates, deletion, and info.
    """

    # Print the banner when group is called
    if ctx.invoked_subcommand:
        render_command_banner(
            "👤 User Command Group",
            "Manage user creation, listing, authentication, and updates."
        )


# 🔐 CLI Commands: Authentication ────────────────────────────
@user.command()
@click.option('--email', prompt="📧 Email")
@click.option('--password', prompt="🔑 Password", hide_input=True)
def login(email, password):
    """🔐 Log in to the CRM system."""
    render_command_banner("Log In", "Authenticate and start a new session.")
    click.secho("🔐 Attempting to log in...", fg="cyan")
    login_user(email, password)


@user.command()
def logout():
    """🚪 Log out of the current session."""
    render_command_banner("Log Out", "Terminate your current authenticated session.")
    click.secho("🚪 Logging out...", fg="cyan")
    logout_user()


# 📝 CLI Commands: User Registration ───────────────────────────
@user.command(name="register-admin")
def register_admin():
    """👑 Register the first admin user (role: 'gestion')."""
    render_command_banner("Register Admin",
                          "Create the first administrative user with gestion privileges.")
    click.secho("👑 Registering a new admin user...", fg="cyan")
    name = click.prompt("🧑 Name")
    email = click.prompt("📧 Email")
    password = click.prompt("🔑 Password", hide_input=True, confirmation_prompt=True)
    role = 'gestion'
    register_user_logic(name, email, password, role)


@user.command(name="register-user")
@attach_sentry_user
@role_required(["gestion"])
def register_user():
    """➕ Register a new user (requires 'gestion' privileges)."""
    render_command_banner("Register User", "Add a new user and assign their access role.")
    click.secho("➕ Registering a new user...", fg="cyan")
    name = click.prompt("🧑 Name")
    email = click.prompt("📧 Email")
    password = click.prompt("🔑 Password", hide_input=True, confirmation_prompt=True)
    role = click.prompt("🥉 Role", type=click.Choice(['commercial', 'gestion', 'support']))
    register_user_logic(name, email, password, role)


# 🛠️ CLI Commands: User Management ──────────────────────────
@user.command(name="update-user-role")
@attach_sentry_user
@role_required(["gestion"])
def update_user_role():
    """🛠️ Change a user's role (requires 'gestion' privileges)."""
    render_command_banner("Update User Role", "Change the access level of an existing user.")
    try:
        user_id = click.prompt("🔹 Enter user ID to modify", type=int)
    except click.Abort:
        click.secho("❌ Aborted.", fg="red")
        return

    role = click.prompt(
        "🥉 Enter new role",
        type=click.Choice(['commercial', 'gestion', 'support'], case_sensitive=False)
    )

    if update_user_role_logic(user_id=user_id, role=role):
        click.secho(f"✅ Role of user {user_id} updated to '{role}'.", fg="green")
    else:
        click.secho(f"❌ Failed to update role for user {user_id}. User may not exist or an error occurred.", fg="red")


@user.command(name="delete")
@attach_sentry_user
@role_required(["gestion"])
def delete_user():
    """🗑️ Delete a user by their ID (requires 'gestion' privileges)."""
    render_command_banner("Delete User", "Remove a user account from the system.")
    try:
        user_id = click.prompt("🔹 Enter the ID of the user to delete", type=int)
        if delete_user_by_id(user_id):
            click.secho(f"✅ User with ID {user_id} was successfully deleted.", fg="green")
        else:
            click.secho(f"⚠️ No user found with ID {user_id}.", fg="yellow")
    except Exception as e:
        click.secho(f"❌ Error deleting user: {str(e)}", fg="red")


# 📋 CLI Commands: Information ───────────────────────────
@user.command()
@role_required(["commercial", "gestion", "support"])
def list_users():
    """📋 Display a list of all registered users."""
    render_command_banner("List Users", "Display all registered users and their roles.")
    click.secho("📋 Listing all users...", fg="cyan")
    list_users_logic()


@user.command(name="list-details")
@role_required(["gestion", "commercial", "support"])
def list_user_details():
    """🔍 Show detailed information for a specific user."""
    render_command_banner("User Details", "Display full event information.")
    list_user_details_logic()


@user.command(name="whoami")
def whoami():
    """👋 Show the currently logged-in user."""
    render_command_banner("Who Am I", "Display the currently authenticated user's information.")
    click.secho("👋 Fetching your user information...", fg="cyan")
    get_logged_user_info()
