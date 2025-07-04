# ─── 🎨 Visual Imports ────────────────────────────────────────────────
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from pyfiglet import Figlet

# ─── 🧠 Application Imports ───────────────────────────────────────────
from Epic_events.database import init_db
from Epic_events.cli import cli

# ─── 🌍 External Imports ───────────────────────────────────────────
import sentry_sdk
import os

# 🔐 Initialize Sentry
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),  # 🔐 Your DSN is securely loaded from .env
    send_default_pii=True,        # 🛡️ Include user data (e.g., emails) if set
    environment="production",     # 🌍 Useful to separate dev vs prod
    traces_sample_rate=1.0        # ⚡ Optional: Enables performance monitoring
)

# ─── 🖥️ Console Setup ─────────────────────────────────────────────────
console = Console()


# ─── 🚀 Main Entry Point ──────────────────────────────────────────────
def main():
    # 📂 Initialize the database
    init_db()
    # ✅ Show styled startup success panel
    console.print(
        Panel.fit(
            "[bold green]Tables created successfully.[/bold green]",
            title="📦 [bold magenta]Startup Complete[/bold magenta]",
            border_style="green"
        )
    )
    # 🔠 Generate and display a centered ASCII banner
    figlet = Figlet(font="slant")
    banner = figlet.renderText("Epic Events CRM")
    console.print(Align.center(banner), style="bold cyan")

    # 💬 Welcome panel (below banner)
    welcome_panel = Panel(
        Text(
            "Welcome to the Epic Events CRM.\n"
            "Type --help after any command for more info.",
            justify="center",
            style="yellow"
        ),
        title="[bold magenta]🚀 Epic Events[/bold magenta]",
        subtitle="[italic cyan]Your Command-Line CRM[/italic cyan]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(welcome_panel)

    # 💻 Launch the CLI application
    cli()


# ─── 🔁 Run as script ─────────────────────────────────────────────────
if __name__ == "__main__":
    main()
