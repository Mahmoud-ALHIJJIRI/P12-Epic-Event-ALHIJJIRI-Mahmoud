# ─── External Imports ───────────────────────────────────────────────
"""
🎨 Rich Styling Utilities for Epic Events CRM

This module defines table styling constants and a helper function to build
styled Rich tables used across the CLI interface for consistent formatting.
"""

# 📦 External Imports ───────────────────────────────────────────────
from rich import box
from rich.table import Table


# 🎨 RICH STYLING CONSTANTS ──────────────────────────────────────────
DEFAULT_BOX = box.MINIMAL_DOUBLE_HEAD
HEADER_STYLE = "bold magenta"
TITLE_STYLE = "bold cyan"


# 📋 TABLE BUILDER ───────────────────────────────────────────────────
def build_table(title: str, columns: list[str]) -> "Table":
    """
    Build and return a styled Rich table with a title and defined column headers.

    Args:
        title (str): Title of the table.
        columns (list[str]): List of column header labels.

    Returns:
        Table: A configured Rich Table object.
    """
    table = Table(
        title=f"📋 [{TITLE_STYLE}]{title}[/{TITLE_STYLE}]",
        title_justify="left",
        box=DEFAULT_BOX,
        show_lines=True,
        header_style=HEADER_STYLE,
    )

    for column in columns:
        table.add_column(column)

    return table
