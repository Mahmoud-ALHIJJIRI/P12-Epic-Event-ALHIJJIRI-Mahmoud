from Epic_events.database import init_db
from Epic_events.cli import cli

if __name__ == "__main__":
    init_db()
    cli()
    print("✅ Tables created successfully.")
