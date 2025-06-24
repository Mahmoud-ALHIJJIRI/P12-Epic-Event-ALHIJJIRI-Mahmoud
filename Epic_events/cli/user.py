import click
from Epic_events.auth.service import register_user, login_user, get_logged_user_info


@click.command()
@click.option('--name', prompt=True)
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
@click.option('--role', prompt=True, type=click.Choice(['commercial', 'gestion', 'support']))
def register(name, email, password, role):
    register_user(name, email, password, role)


@click.command()
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(email, password):
    login_user(email, password)


@click.command()
def whoami():
    get_logged_user_info()
