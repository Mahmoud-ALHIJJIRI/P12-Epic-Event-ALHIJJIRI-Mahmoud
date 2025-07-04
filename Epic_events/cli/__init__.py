#
"""
🎯 CLI Entry Point for Epic Events CRM

This file defines the root Click group and integrates all subcommands (user, client, contract, event)
into a unified interface for command-line interaction.
"""

# ─── External Imports ───────────────────────────────────────────────
import rich_click as click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# ─── Internal Imports ───────────────────────────────────────────────
from .user import user
from .client import client
from .contract import contract
from .event import event


# 🚀 ROOT CLI GROUP ───────────────────────────────────────────────────
@click.group(cls=click.RichGroup)
@click.pass_context
def cli(ctx):
    """
    📦 Epic Events CRM CLI

    Use this interface to manage users, clients, contracts, and events.
    Type --help after any command for detailed usage information.
    """
    # No banner or panel needed here anymore (handled in main.py)
    pass


# 👤 Add user command group (login, registration, etc.)
cli.add_command(user)
# 🧑‍💼 Add client command group (CRUD for client data)
cli.add_command(client)
# 📋 Add contract command group (create, update, filter contracts)
cli.add_command(contract)
# 🎉 Add event command group (assign support, view event details)
cli.add_command(event)
