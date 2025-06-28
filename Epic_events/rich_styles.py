# ─── External Imports ───────────────────────────────────────────────
from rich import box
from rich.table import Table


# 🎨 RICH STYLING CONSTANTS ──────────────────────────────────────────
DEFAULT_BOX = box.MINIMAL_DOUBLE_HEAD
HEADER_STYLE = "bold magenta"
TITLE_STYLE = "bold cyan"


# 📋 TABLE BUILDER ───────────────────────────────────────────────────
def build_table(title: str, columns: list[str]) -> "Table":
    """
    Build a styled Rich table with a title and column headers.
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
