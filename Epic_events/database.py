from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Read the DATABASE_URL variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
