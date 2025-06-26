# Import libraries
import jwt

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
    """Save the JWT token to the token file."""
    print(f"[DEBUG] Writing token to {TOKEN_FILE.resolve()}")
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(token.strip())


# -------------------------
# 📤 Load Token
# -------------------------
def load_token() -> str:
    """Load the JWT token from file."""
    if not TOKEN_FILE.exists():
        raise Exception("❌ You are not logged in. Please login first.")

    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        token = f.read().strip()

    if not token:
        raise Exception("❌ Token is empty. Please login again.")

    return token


# -------------------------
# 🔓 Decode Token
# -------------------------
def decode_token(token: str) -> dict:
    """Decode the JWT token and return its payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise Exception("⚠️ Token expired. Please login again.")
    except InvalidTokenError as e:
        raise Exception(f"❌ Invalid token: {str(e)}")


# -------------------------
# 👤 Get Current User Info
# -------------------------
def get_current_user() -> dict:
    """Helper that loads and decodes the token in one step."""
    token = load_token()
    return decode_token(token)
