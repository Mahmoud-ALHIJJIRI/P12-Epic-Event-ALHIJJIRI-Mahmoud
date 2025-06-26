import click
from Epic_events.service.user_service import (register_user_logic, login_user,
                                              get_logged_user_info, list_users_logic,
                                              logout_user, delete_user_by_id)
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
@role_required(["commercial", "gestion", "support"])
def list_users():
    """List all users in the system."""
    list_users_logic()


@click.command()
def whoami():
    """Who is the logged in"""
    get_logged_user_info()
