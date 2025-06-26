from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
import enum
from .database import Base


# Define role types using Python Enum
class UserRole(enum.Enum):
    commercial = "commercial"
    gestion = "gestion"
    support = "support"


# User model
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Reminder: hash before storing
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)
    # Relationships
    clients = relationship("Client", back_populates="commercial", passive_deletes=True)
    contracts = relationship("Contract", back_populates="commercial", passive_deletes=True)
    events = relationship("Event", back_populates="support")


# Client model
class Client(Base):
    __tablename__ = 'clients'

    client_id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    created_date = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    last_contact = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC),
                          nullable=False)
    # Foreign key: which commercial is assigned to this client
    commercial_id = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    # Relationships
    commercial = relationship("User", back_populates="clients")
    contracts = relationship("Contract", back_populates="client", passive_deletes=True)
    events = relationship("Event", back_populates="client")


# Contract model
class Contract(Base):
    __tablename__ = 'contracts'

    contract_id = Column(Integer, primary_key=True)

    amount_total = Column(Integer, default=0, nullable=False)
    amount_due = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    is_signed = Column(Boolean, nullable=False, default=False)
    # Foreign keys
    client_id = Column(Integer, ForeignKey('clients.client_id', ondelete='RESTRICT'), nullable=False)
    commercial_id = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    # Relationships
    client = relationship("Client", back_populates="contracts")
    commercial = relationship("User", back_populates="contracts")
    events = relationship("Event", back_populates="contract")


# Event model
class Event(Base):
    __tablename__ = 'events'

    event_id = Column(Integer, primary_key=True)
    event_name = Column(String, nullable=False)
    start_date = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    end_date = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    location = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    # Foreign Keys
    client_id = Column(Integer, ForeignKey('clients.client_id', ondelete='RESTRICT'), nullable=False)
    contract_id = Column(Integer, ForeignKey('contracts.contract_id', ondelete='RESTRICT'), nullable=False)
    support_id = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    # Relationships
    client = relationship("Client", back_populates="events")
    contract = relationship("Contract", back_populates="events")
    support = relationship("User", back_populates="events")
