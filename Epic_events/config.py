import os
from dotenv import load_dotenv
from pathlib import Path

# 📁 Define the paths
env_path = Path(__file__).resolve().parent.parent / ".env"
token_path = os.getenv("TOKEN_FILE_PATH", "~/.epic_crm_token")

# 🔐 Load environment variables from the .env file into os.environ
load_dotenv(dotenv_path=env_path)

# 🔑 Secret key used for signing JWT tokens.
# Should be set in .env for production security.
SECRET_KEY = os.getenv("SECRET_KEY")

# 🗄️ PostgreSQL connection URL, used to initialize SQLAlchemy.
DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL:", DATABASE_URL)
# 📂 Path to the local token file for storing the JWT token.
TOKEN_FILE = Path(token_path).expanduser()
