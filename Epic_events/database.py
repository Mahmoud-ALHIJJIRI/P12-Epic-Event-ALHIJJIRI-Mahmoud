"""
🗄️ Database Configuration for Epic Events CRM

This module sets up the SQLAlchemy engine, session, and base class.
It also provides a function to initialize the database schema using all defined models.
"""

# ─── External Imports ───────────────────────────────────────────────
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# ⚙️ Load Configuration ─────────────────────────────────────────────
from .config import DATABASE_URL  # Cleanly imported from config


# 🛠️ DATABASE ENGINE & SESSION ──────────────────────────────────────
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# 🧱 BASE ORM CLASS ──────────────────────────────────────────────────
Base = declarative_base()


# 🚀 INIT DATABASE SCHEMA ────────────────────────────────────────────
def init_db():
    """
    Initialize the database by importing all models and creating tables if they do not exist.
    """
    from .models import User, Client, Contract, Event  # Ensure models are loaded
    Base.metadata.create_all(bind=engine)
