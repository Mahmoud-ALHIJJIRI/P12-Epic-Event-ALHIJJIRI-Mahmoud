#
"""
🛠️ Utility functions for the Epic Events CRM system.

This module handles local JWT token storage, loading, decoding, and user context extraction.
"""

# Import libraries
import jwt
from click import ClickException

# Internal imports
from pathlib import Path
from jwt import ExpiredSignatureError, InvalidTokenError
from Epic_events.config import SECRET_KEY

# Path to store the token locally
TOKEN_FILE = Path.home() / ".epic_crm_token"
ALGORITHM = "HS256"


# -------------------------
# 💾 Save Token
# -------------------------
def save_token(token: str):
    """
    Save the JWT token to a file on the user's system.

    Args:
        token (str): The JWT token string to be saved.
    """
    # 💾 Write token to a hidden file in the home directory
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(token.strip())


# -------------------------
# 📤 Load Token
# -------------------------
def load_token() -> str:
    """
    Load the JWT token from the local token file.

    Returns:
        str: The JWT token string.

    Raises:
        Exception: If token file is missing or empty.
    """
    # 📂 Check if token file exists
    if not TOKEN_FILE.exists():
        raise ClickException("❌ You are not logged in. Please login first.")

    # 📄 Read token from file and strip whitespace
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        token = f.read().strip()

    # 🚫 Raise error if token is empty
    if not token:
        raise ClickException("❌ Token is empty. Please login again.")

    return token


# -------------------------
# 🔓 Decode Token
# -------------------------
def decode_token(token: str) -> dict:
    """
    Decode a JWT token using the project's secret key.

    Args:
        token (str): The JWT token string.

    Returns:
        dict: The decoded payload.

    Raises:
        Exception: If the token is expired or invalid.
    """
    try:
        # 🔐 Decode token using HS256 and SECRET_KEY
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # ⌛ Token expired
        raise ClickException("⚠️ Token expired. Please login again.")
    except InvalidTokenError as e:
        # ❗ Invalid token
        raise ClickException(f"❌ Invalid token: {str(e)}")


# -------------------------
# 👤 Get Current User Info
# -------------------------
def get_current_user() -> dict:
    """
    Retrieve the currently logged-in user's data from the stored JWT.

    Returns:
        dict: Payload containing user ID, role, and other metadata.
    """
    # 📥 Load token from local file
    token = load_token()
    # 🔍 Decode and return user data
    return decode_token(token)
