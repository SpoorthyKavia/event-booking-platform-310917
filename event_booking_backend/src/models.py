"""
Database models for Event Booking System.
"""
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime

from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_organizer = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    events = relationship("Event", back_populates="organizer")
    bookings = relationship("Booking", back_populates="user")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    total_seats = Column(Integer)
    available_seats = Column(Integer)
    ticket_price = Column(Float, default=0)
    status = Column(String, default="published")  # draft/published/cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    organizer_id = Column(Integer, ForeignKey("users.id"))

    organizer = relationship("User", back_populates="events")
    bookings = relationship("Booking", back_populates="event")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    quantity = Column(Integer, default=1)
    total_price = Column(Float)
    booking_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="confirmed")
    payment_status = Column(String, default="pending")  # pending/paid/failed
    payment_reference = Column(String, nullable=True)

    user = relationship("User", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
