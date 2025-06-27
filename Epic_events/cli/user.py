import click
from Epic_events.service.user_service import (register_user_logic, login_user,
                                              get_logged_user_info, list_users_logic,
                                              logout_user, delete_user_by_id, update_user_role_logic)
from Epic_events.auth.permissions import role_required


@click.command()
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(email, password):
    """Login user."""
    login_user(email, password)


@click.command()
def logout():
    """Logout User"""
    logout_user()


@click.command()
def register_admin():
    """Register Admin."""
    name = click.prompt("Name")
    email = click.prompt("Email")
    password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
    role = 'gestion'

    register_user_logic(name, email, password, role)


@click.command()
@role_required(["gestion"])
def register_user():
    """Register a new user (gestion only)."""
    name = click.prompt("Name")
    email = click.prompt("Email")
    password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
    role = click.prompt("Role", type=click.Choice(['commercial', 'gestion', 'support']))

    register_user_logic(name, email, password, role)


@click.command()
@role_required(["gestion"])
def delete_user():
    """Delete a user by ID (gestion only)."""
    try:
        user_id = click.prompt("Enter the ID of the user to delete", type=int)
        deleted = delete_user_by_id(user_id)
        if deleted:
            click.echo(f"✅ User with ID {user_id} was successfully deleted.")
        else:
            click.echo(f"⚠️ No user found with ID {user_id}.")
    except Exception as e:
        click.echo(f"❌ Error deleting user: {str(e)}")


@click.command()
@role_required(["gestion"])  # Manager-only access
def update_user_role():
    """Change a user's role by prompting for ID and new role (Manager only)."""
    try:
        user_id = click.prompt("Enter user ID to modify", type=int)
    except click.Abort:
        click.echo("❌ Aborted.")
        return

    # Prompt for the role using a case-insensitive choice
    role = click.prompt("Enter new role", type=click.Choice(
        ['commercial', 'gestion', 'support'], case_sensitive=False))

    if update_user_role_logic(user_id=user_id, role=role):
        click.echo(f"✅ Role of user {user_id} updated to '{role}'.")
    else:
        click.echo(f"❌ Failed to update role for user {user_id}. "
                   f"The user may not exist or an error occurred.")


@click.command()
@role_required(["commercial", "gestion", "support"])
def list_users():
    """List all users in the system."""
    list_users_logic()


@click.command()
def whoami():
    """Who is the logged in"""
    get_logged_user_info()
