import click
from Epic_events.auth.service import register_user, login_user, get_logged_user_info
from Epic_events.auth.permissions import role_required


@click.command()
@role_required(["gestion"])
def register_user():
    """Register a new user (gestion only)."""
    name = click.prompt("Name")
    email = click.prompt("Email")
    password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
    role = click.prompt("Role", type=click.Choice(['commercial', 'gestion', 'support']))

    register_user(name, email, password, role)


@click.command()
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(email, password):
    """Login user."""
    login_user(email, password)


@click.command()
def whoami():
    """Who is the logged in"""
    get_logged_user_info()
