import functools
import click
from .utils import get_current_user


def role_required(allowed_roles):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                user = get_current_user()
                user_role = user.get("role")
                if user_role not in allowed_roles:
                    raise Exception(f"Permission denied: role '{user_role}' is not allowed.")
            except Exception as e:
                click.echo(f"❌ Access denied: {e}")
                return
            return f(*args, **kwargs)
        return wrapper
    return decorator
