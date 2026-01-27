"""
Seed script for mock data—ONLY run in dev!

Populate roles, admin, and some demo events/users/bookings.
"""
from sqlalchemy.orm import Session
from .models import User, Event, Booking, Role, UserRole
from .auth import get_password_hash
from datetime import datetime, timedelta

# PUBLIC_INTERFACE
def seed_db(db: Session):
    """Seed DB with basic roles, admin, users and events."""

    # Check if data exists
    if db.query(User).count() > 0:
        return

    role_admin = Role(name="admin")
    role_organizer = Role(name="organizer")
    db.add_all([role_admin, role_organizer])
    db.commit()

    admin = User(
        email="admin@evtbooker.com",
        hashed_password=get_password_hash("adminpass"),
        full_name="Admin User",
        is_admin=True,
    )
    organizer = User(
        email="org1@evtbooker.com",
        hashed_password=get_password_hash("orgpass"),
        full_name="Organizer One",
        is_organizer=True,
    )
    user = User(
        email="user1@evtbooker.com",
        hashed_password=get_password_hash("userpass"),
        full_name="Demo User",
    )
    db.add_all([admin, organizer, user])
    db.commit()

    db.add(UserRole(user_id=admin.id, role_id=role_admin.id))
    db.add(UserRole(user_id=organizer.id, role_id=role_organizer.id))

    ev1 = Event(
        title="Tech Conference",
        description="A modern event for developers.",
        location="Conference Hall 3",
        start_time=datetime.utcnow() + timedelta(days=10),
        end_time=datetime.utcnow() + timedelta(days=10, hours=4),
        total_seats=100,
        available_seats=100,
        ticket_price=49.99,
        organizer_id=organizer.id
    )
    db.add(ev1)
    db.commit()
    db.add(Booking(
        user_id=user.id,
        event_id=ev1.id,
        quantity=2,
        total_price=99.98,
        status="confirmed",
        payment_status="paid",
        payment_reference="MOCKPAYMENT1"
    ))
    db.commit()
