from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL  # Now cleanly imported from config

# Initialize engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Base class for ORM models
Base = declarative_base()


def init_db():
    from .models import User, Client, Contract, Event  # Ensure model imports for table creation
    Base.metadata.create_all(bind=engine)
