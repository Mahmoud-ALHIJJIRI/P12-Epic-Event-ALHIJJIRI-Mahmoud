# ─── External Imports ───────────────────────────────────────────────
import functools
import click

# ─── Internal Imports ───────────────────────────────────────────────
from .utils import get_current_user
from Epic_events.database import SessionLocal


# 🛡️ ROLE-BASED ACCESS DECORATOR ─────────────────────────────────────
def role_required(allowed_roles):
    """
    Restrict access to users with specified roles.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                user = get_current_user()
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
    Restrict access to the owner of a specific resource, unless role is 'gestion'.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                user = get_current_user()
                user_id = user.get("sub")
                user_role = user.get("role")

                # 👥 Allow gestion to bypass ownership check
                if user_role == "gestion":
                    return f(*args, **kwargs)

                # 🔍 Extract entity ID from command args
                entity_id = kwargs.get(id_arg)
                if not entity_id:
                    raise Exception(f"Missing required argument: '{id_arg}'.")

                pk_column = list(model.__table__.primary_key.columns)[0]
                pk_attr = getattr(model, pk_column.name)

                # 🧾 Query entity from DB
                db_session = SessionLocal()
                entity = db_session.query(model).filter(pk_attr == entity_id).first()
                db_session.close()

                if not entity:
                    raise Exception(f"{model.__name__} with ID {entity_id} not found.")

                owner_id = getattr(entity, owner_field)

                if int(owner_id) != int(user_id):
                    raise Exception("You do not have ownership over this resource.")

            except Exception as e:
                click.echo(f"❌ Access denied: {e}")
                return

            return f(*args, **kwargs)
        return wrapper
    return decorator
