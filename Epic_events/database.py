# ─── External Imports ───────────────────────────────────────────────
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ─── Internal Imports ───────────────────────────────────────────────
from .config import DATABASE_URL  # Cleanly imported from config


# 🛠️ DATABASE ENGINE & SESSION ──────────────────────────────────────
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# 🧱 BASE ORM CLASS ──────────────────────────────────────────────────
Base = declarative_base()


# 🚀 INIT DATABASE SCHEMA ────────────────────────────────────────────
def init_db():
    """
    Import models and create tables if they don't exist.
    """
    from .models import User, Client, Contract, Event  # Ensure models are loaded
    Base.metadata.create_all(bind=engine)
