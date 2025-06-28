# 🧩 External Imports ────────────────────────────────────────────────
import click

# 🏗️ Internal Imports ────────────────────────────────────────────────
from Epic_events.service.user_service import (
    register_user_logic,
    login_user,
    logout_user,
    get_logged_user_info,
    list_users_logic,
    delete_user_by_id,
    update_user_role_logic
)
from Epic_events.auth.permissions import role_required


# 🔐 CLI Commands: Authentication ─────────────────────────────────────
@click.command()
@click.option('--email', prompt="📧 Email")
@click.option('--password', prompt="🔑 Password", hide_input=True)
def login(email, password):
    """🔐 Log in to the CRM system."""
    click.secho("🔐 Attempting to log in...", fg="cyan")
    login_user(email, password)


@click.command()
def logout():
    """🚪 Log out of the current session."""
    click.secho("🚪 Logging out...", fg="cyan")
    logout_user()


# 📝 CLI Commands: User Registration ─────────────────────────────────
@click.command()
def register_admin():
    """👑 Register the first admin user (role: 'gestion')."""
    click.secho("👑 Registering a new admin user...", fg="cyan")
    name = click.prompt("🧑 Name")
    email = click.prompt("📧 Email")
    password = click.prompt("🔑 Password", hide_input=True, confirmation_prompt=True)
    role = 'gestion'

    register_user_logic(name, email, password, role)


@click.command()
@role_required(["gestion"])
def register_user():
    """➕ Register a new user (requires 'gestion' privileges)."""
    click.secho("➕ Registering a new user...", fg="cyan")
    name = click.prompt("🧑 Name")
    email = click.prompt("📧 Email")
    password = click.prompt("🔑 Password", hide_input=True, confirmation_prompt=True)
    role = click.prompt("🧩 Role", type=click.Choice(['commercial', 'gestion', 'support']))

    register_user_logic(name, email, password, role)


# 🛠️ CLI Commands: User Management ───────────────────────────────────
@click.command()
@role_required(["gestion"])
def update_user_role():
    """🛠️ Change a user's role (requires 'gestion' privileges)."""
    try:
        user_id = click.prompt("🔢 Enter user ID to modify", type=int)
    except click.Abort:
        click.secho("❌ Aborted.", fg="red")
        return

    role = click.prompt(
        "🧩 Enter new role",
        type=click.Choice(['commercial', 'gestion', 'support'], case_sensitive=False)
    )

    if update_user_role_logic(user_id=user_id, role=role):
        click.secho(f"✅ Role of user {user_id} updated to '{role}'.", fg="green")
    else:
        click.secho(f"❌ Failed to update role for user {user_id}. User may not exist or an error occurred.", fg="red")


@click.command()
@role_required(["gestion"])
def delete_user():
    """🗑️ Delete a user by their ID (requires 'gestion' privileges)."""
    try:
        user_id = click.prompt("🔢 Enter the ID of the user to delete", type=int)
        if delete_user_by_id(user_id):
            click.secho(f"✅ User with ID {user_id} was successfully deleted.", fg="green")
        else:
            click.secho(f"⚠️ No user found with ID {user_id}.", fg="yellow")
    except Exception as e:
        click.secho(f"❌ Error deleting user: {str(e)}", fg="red")


# 📋 CLI Commands: Information ───────────────────────────────────────
@click.command()
@role_required(["commercial", "gestion", "support"])
def list_users():
    """📋 Display a list of all registered users."""
    click.secho("📋 Listing all users...", fg="cyan")
    list_users_logic()


@click.command(name="whoami")
def whoami():
    """🙋 Show the currently logged-in user."""
    click.secho("🙋 Fetching your user information...", fg="cyan")
    get_logged_user_info()
