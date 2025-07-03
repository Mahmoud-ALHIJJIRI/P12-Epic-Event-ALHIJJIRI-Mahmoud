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
    Type --help after any command for more info.
    """
    # No banner or panel needed here anymore (handled in main.py)
    pass

# 👤 USER COMMANDS ───────────────────────────────────────────────────
cli.add_command(user)
# 🧑‍💼 CLIENT COMMANDS ───────────────────────────────────────────────
cli.add_command(client)
# 📋 CONTRACT COMMANDS ───────────────────────────────────────────────
cli.add_command(contract)
# 📋 Event COMMANDS ───────────────────────────────────────────────
cli.add_command(event)
