from datetime import datetime, timedelta, timezone
from typing import Optional
from click import ClickException
from sqlalchemy.exc import IntegrityError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
import click
from rich.table import Table
from rich.console import Console


from sqlalchemy.orm import Session
from Epic_events.config import SECRET_KEY
from Epic_events.database import SessionLocal
from Epic_events.models import User, UserRole
from Epic_events.auth.utils import save_token, load_token, decode_token, get_current_user

ph = PasswordHasher()
ALGORITHM = "HS256"


# -------------------------
# 🧑‍💻 Register User
# -------------------------
def register_user_logic(name, email, password, role):
    """Handles logic for registering a new user."""
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


# -------------------------
# 🔐 Login User
# -------------------------
def login_user(email, password):
    """Handles logic for logging in a user and storing the JWT."""
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
        "sub": str(user.id),
        "name": user.name,
        "role": user.role.value,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)
    }

    try:
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    except jwt.PyJWTError as e:
        click.echo(f"❌ Failed to generate token: {str(e)}")
        session.close()
        return

    try:
        save_token(token)
        click.echo("✅ Logged in successfully.")
    except Exception as e:
        click.echo(f"❌ Failed to write token to file: {str(e)}")
    finally:
        session.close()


# -------------------------
# 👤 Logged in User
# -------------------------
def get_logged_in_user() -> User:
    """
    Returns the SQLAlchemy User object corresponding to the logged-in user,
    based on the JWT token stored in ~/.epic_crm_token.
    """
    payload = get_current_user()
    user_id = payload.get("sub")

    if not user_id:
        raise ClickException("❌ Token is missing user ID (sub claim).")

    session: Session = SessionLocal()
    user: Optional[User] = session.get(User, int(user_id))
    session.close()

    if not user:
        raise ClickException("❌ Logged-in user not found in database.")
    return user


# -------------------------
# 👤 Who Am I
# -------------------------
def get_logged_user_info():
    """Prints info about the currently logged-in user."""
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
    user = session.query(User).get(int(user_id))
    session.close()

    if user:
        click.echo(f"✅ Logged in as: Name: {name}, email: {user.email}, User Role: {role}")
    else:
        click.echo("❌ User not found.")


# -------------------------
# 👤 List users
# -------------------------
def list_users_logic():
    session = SessionLocal()
    console = Console()

    try:
        users = session.query(User).all()

        table = Table(title="📋 All Users")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Email")
        table.add_column("Role")

        for user in users:
            table.add_row(
                str(user.id),
                user.name,
                user.email,
                user.role.value
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
    finally:
        session.close()
