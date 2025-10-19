#
# ─── Module Docstring ──────────────────────────────────────────────────────────────
"""
🔐 Permission decorators for Epic Events CRM.

This module provides decorators to enforce role-based and ownership-based access control,
as well as automatic Sentry user context attachment for error tracking.
"""

# ─── External Imports ───────────────────────────────────────────────
import functools
import click
import sentry_sdk
# ─── Internal Imports ───────────────────────────────────────────────
from .utils import get_current_user
from Epic_events.database import SessionLocal


# 🛡️ ROLE-BASED ACCESS DECORATOR ─────────────────────────────────────
def role_required(allowed_roles):
    """
    Decorator to restrict access based on user roles.

    Args:
        allowed_roles (list): A list of roles permitted to access the decorated function.

    Returns:
        function: A wrapped function that performs role validation before execution.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # 🧾 Retrieve the current user from token/session
                user = get_current_user()
                if not user:
                    click.echo("❌ You are not logged in. Please login first.")
                    return
                # 🛂 Check if user's role is allowed
                user_role = user.get("role")
                if user_role not in allowed_roles:
                    raise Exception(f"Permission denied: '{user_role}' users are not allowed to perform this action.")
            except Exception as e:
                click.echo(f"❌ Access denied: {e}")
                return
            return f(*args, **kwargs)
        return wrapper
    return decorator


# 🔒 OWNER-BASED ACCESS DECORATOR ────────────────────────────────────
def owner_required(model, owner_field: str, id_arg: str = "id"):
    """
    Decorator to restrict access to the owner of a resource or allow 'gestion' role override.

    Args:
        model (Base): SQLAlchemy model representing the resource.
        owner_field (str): The field name on the model that stores the owner's user ID.
        id_arg (str): The CLI argument name used to pass the resource ID (default: 'id').

    Returns:
        function: A wrapped function that performs ownership or role validation.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # 🧾 Get current user's ID and role
                user = get_current_user()
                user_id = user.get("sub")
                user_role = user.get("role")

                # 🛂 Allow 'gestion' role to bypass ownership check
                if user_role == "gestion":
                    return f(*args, **kwargs)

                # 🔍 Fetch resource ID from CLI args
                entity_id = kwargs.get(id_arg)
                if not entity_id:
                    raise Exception(f"Missing required argument: '{id_arg}'.")

                pk_column = list(model.__table__.primary_key.columns)[0]
                pk_attr = getattr(model, pk_column.name)

                # 📄 Retrieve the entity from the database
                db_session = SessionLocal()
                entity = db_session.query(model).filter(pk_attr == entity_id).first()
                db_session.close()

                if not entity:
                    raise Exception(f"{model.__name__} with ID {entity_id} not found.")

                # 🧑‍🤝‍🧑 Compare entity's owner ID to current user's ID
                owner_id = getattr(entity, owner_field)
                if int(owner_id) != int(user_id):
                    raise Exception("You do not have ownership over this resource.")

            except Exception as e:
                click.echo(f"❌ Access denied: {e}")
                return

            return f(*args, **kwargs)
        return wrapper
    return decorator


# 🧠 SENTRY USER CONTEXT DECORATOR ─────────────────────────────────────
def attach_sentry_user(func):
    """
    Decorator to attach the current user's identity to Sentry for error logging context.

    This helps associate logs and exceptions with specific users.
    """
    def wrapper(*args, **kwargs):
        # 🧠 Set Sentry context with current user's details
        user = get_current_user()
        if user:
            sentry_sdk.set_user({
                "id": user["sub"],
                "name": user["name"],
                "role": user["role"]
            })
        return func(*args, **kwargs)
    return wrapper
