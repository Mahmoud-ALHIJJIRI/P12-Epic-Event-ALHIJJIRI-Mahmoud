from rich import box
from rich.table import Table

# Shared box styles
DEFAULT_BOX = box.MINIMAL_DOUBLE_HEAD
HEADER_STYLE = "bold magenta"
TITLE_STYLE = "bold cyan"


# Example function to build styled tables
def build_table(title: str, columns: list[str]) -> "Table":
    from rich.table import Table

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
