# ─── External Imports ───────────────────────────────────────────────
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import click
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from click import ClickException
from rich.console import Console
from rich.panel import Panel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# ─── Internal Imports ───────────────────────────────────────────────
from Epic_events.config import SECRET_KEY
from Epic_events.database import SessionLocal
from Epic_events.models import User, UserRole
from Epic_events.rich_styles import build_table
from Epic_events.auth.utils import save_token, load_token, decode_token, get_current_user

# ─── Constants ──────────────────────────────────────────────────────
ph = PasswordHasher()
ALGORITHM = "HS256"
TOKEN_FILE = Path.home() / ".epic_crm_token"


# ────────────────────────────────────────────────────────────────────
# 👤 USER REGISTRATION
# ────────────────────────────────────────────────────────────────────
def register_admin_logic(name, email, password, role):
    """Register the initial admin (with role 'gestion')."""
    session = SessionLocal()

    try:
        user_role_enum = UserRole(role)
    except ValueError:
        click.echo(f"❌ Invalid role '{role}'.")
        session.close()
        return

    hashed_pw = ph.hash(password)
    user = User(name=name, email=email, password=hashed_pw, role=user_role_enum)

    try:
        session.add(user)
        session.commit()
        click.echo("✅ Admin registered successfully!")
    except IntegrityError:
        session.rollback()
        click.echo("❌ Email already in use.")
    finally:
        session.close()


def register_user_logic(name, email, password, role):
    """Register a new user with the given role."""
    session = SessionLocal()

    try:
        user_role_enum = UserRole(role)
    except ValueError:
        click.echo(f"❌ Invalid role '{role}'.")
        session.close()
        return

    hashed_pw = ph.hash(password)
    user = User(name=name, email=email, password=hashed_pw, role=user_role_enum)

    try:
        session.add(user)
        session.commit()
        click.echo("✅ User registered successfully!")
    except IntegrityError:
        session.rollback()
        click.echo("❌ Email already in use.")
    finally:
        session.close()


# ────────────────────────────────────────────────────────────────────
# 🔐 LOGIN / AUTH / LOGOUT
# ────────────────────────────────────────────────────────────────────

def login_user(email, password):
    """Authenticate user and store JWT."""
    session = SessionLocal()
    user = session.query(User).filter_by(email=email).first()

    if not user:
        click.echo("❌ User not found.")
        session.close()
        return

    try:
        ph.verify(user.password, password)
    except VerifyMismatchError:
        click.echo("❌ Incorrect password.")
        session.close()
        return

    token_data = {
        "sub": str(user.user_id),
        "name": user.name,
        "role": user.role.value,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)
    }

    try:
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        save_token(token)
        click.echo("✅ Logged in successfully.")
    except jwt.PyJWTError as e:
        click.echo(f"❌ Token generation failed: {str(e)}")
    except Exception as e:
        click.echo(f"❌ Failed to save token: {str(e)}")
    finally:
        session.close()


def logout_user():
    """Delete the stored JWT token."""
    if not TOKEN_FILE.exists():
        raise Exception("❌ No user is currently logged in.")

    try:
        TOKEN_FILE.unlink()
        print("✅ Successfully logged out.")
    except Exception as e:
        raise Exception(f"❌ Error while logging out: {str(e)}")


# ────────────────────────────────────────────────────────────────────
# 👤 CURRENT USER INFO
# ────────────────────────────────────────────────────────────────────

def get_logged_in_user() -> User:
    """
    Return the current user object based on the stored JWT token.
    """
    payload = get_current_user()
    user_id = payload.get("sub")

    if not user_id:
        raise ClickException("❌ Token missing user ID (sub claim).")

    session: Session = SessionLocal()
    user: Optional[User] = session.get(User, int(user_id))
    session.close()

    if not user:
        raise ClickException("❌ Logged-in user not found in database.")
    return user


def get_logged_user_info():
    """Print information about the currently logged-in user."""
    try:
        token = load_token()
        payload = decode_token(token)
    except Exception as e:
        click.echo(str(e))
        return

    user_id = payload.get("sub")
    role = payload.get("role")
    name = payload.get("name")

    if not user_id:
        click.echo("❌ Token is missing user ID.")
        return

    session = SessionLocal()
    user = session.get(User, int(user_id))
    session.close()

    if user:
        click.echo(f"✅ Logged in as: Name: {name}, Email: {user.email}, Role: {role}")
    else:
        click.echo("❌ User not found.")


# ────────────────────────────────────────────────────────────────────
# 👤 Update USER INFO
# ────────────────────────────────────────────────────────────────────
def delete_user_by_id(user_id: int):
    """Delete a user by ID. Returns True if successful, False otherwise."""
    session: Session = SessionLocal()

    try:
        user = session.get(User, user_id)
        if not user:
            return False

        session.delete(user)
        session.commit()
        return True

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def update_user_role_logic(user_id: int, role: str):
    """
    Update the role of a given user.

    Args:
        user_id: ID of the user to update.
        role: New role to assign.

    Returns:
        True if update succeeded, False otherwise.
    """
    session: Session = SessionLocal()
    try:
        user = session.get(User, user_id)
        if not user:
            return False

        user.role = UserRole(role)
        session.commit()
        return True

    except Exception as e:
        session.rollback()
        click.echo(f"❌ Error updating role: {e}", err=True)
        return False

    finally:
        session.close()


# ────────────────────────────────────────────────────────────────────
# 📋 USER LISTING / ADMIN FUNCTIONS
# ────────────────────────────────────────────────────────────────────

def list_users_logic():
    session = SessionLocal()
    console = Console()

    try:
        users = session.query(User).all()
        if not users:
            console.print("[yellow]⚠️ No users found.[/yellow]")
            return

        table = build_table("Registered Users", ["👤 ID", "🧑 Name", "📧 Email", "🔐 Role"])

        for user in users:
            table.add_row(
                str(user.user_id),
                user.name,
                user.email,
                user.role.value.capitalize()
            )

        console.print(Panel.fit(table, border_style="cyan", title="User Overview"))

    finally:
        session.close()
