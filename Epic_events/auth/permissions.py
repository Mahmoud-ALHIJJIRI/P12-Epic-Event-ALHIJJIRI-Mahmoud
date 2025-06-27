import functools
import click
from .utils import get_current_user
from Epic_events.database import SessionLocal


def role_required(allowed_roles):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                user = get_current_user()
                user_role = user.get("role")
                if user_role not in allowed_roles:
                    raise Exception(f"Permission denied:'{user_role}' users are not allowed to this action.")
            except Exception as e:
                click.echo(f"❌ Access denied: {e}")
                return
            return f(*args, **kwargs)
        return wrapper
    return decorator


def owner_required(model, owner_field: str, id_arg: str = "id"):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                user = get_current_user()
                user_id = user.get("user_id")
                user_name = user.get("name")
                user_role = user.get("role")
                # 👇 If user is gestion, allow without ownership check

                if user_role == "gestion":
                    return f(*args, **kwargs)

                if not user_id or not user_role:
                    raise Exception(f"Hey {user_name}! You don't have the permission to do this action")

                # Get entity ID from the command argument
                entity_id = kwargs.get(id_arg)
                if not entity_id:
                    raise Exception(f"Missing required argument: '{id_arg}'.")

                # Query the entity
                db_session = SessionLocal()
                entity = db_session.query(model).filter(model.id == entity_id).first()
                db_session.close()

                if not entity:
                    raise Exception(f"{model.__name__} with ID {entity_id} not found.")

                owner_id = getattr(entity, owner_field)
                if owner_id != user_id:
                    raise Exception("You do not have ownership over this resource.")

            except Exception as e:
                click.echo(f"❌ Access denied: {e}")
                return

            return f(*args, **kwargs)
        return wrapper
    return decorator
