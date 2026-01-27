"""
Main API routes for Event Booking System: auth, event CRUD, event listing/filtering, booking, payment mock, admin, and notification webhooks (stub).
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db import get_db
from ..models import User, Event, Booking
from ..schemas import (
    UserCreate, UserOut, UserLogin,
    EventCreate, EventOut, BookingCreate, BookingOut
)
from ..auth import (
    get_password_hash, verify_password, create_access_token, decode_access_token,
)
from ..notify import send_email_stub
from ..payment import process_mock_payment

router = APIRouter()

def get_current_user(token: str = Query(..., alias="access_token"), db: Session = Depends(get_db)):
    """Extract current user from JWT token."""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user = db.query(User).get(payload.get("user_id"))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ---- AUTH ----

# PUBLIC_INTERFACE
@router.post("/auth/register", response_model=UserOut, tags=["auth"], summary="Register new user")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "Email already registered")
    dbuser = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
    )
    db.add(dbuser)
    db.commit()
    db.refresh(dbuser)
    send_email_stub(dbuser.email, "Welcome!", "Welcome to Event Booking!")
    return dbuser

# PUBLIC_INTERFACE
@router.post("/auth/login", tags=["auth"], summary="Login, returns JWT access token")
def login(user: UserLogin, db: Session = Depends(get_db)):
    dbuser = db.query(User).filter(User.email == user.email).first()
    if not dbuser or not verify_password(user.password, dbuser.hashed_password):
        raise HTTPException(401, "Incorrect email or password")
    token = create_access_token(data={"user_id": dbuser.id})
    return {"access_token": token}

# ---- EVENTS ----

# PUBLIC_INTERFACE
@router.post("/events/", response_model=EventOut, tags=["events"], summary="Create new event")
def create_event(event: EventCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_organizer and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    db_event = Event(
        title=event.title,
        description=event.description,
        location=event.location,
        start_time=event.start_time,
        end_time=event.end_time,
        total_seats=event.total_seats,
        available_seats=event.total_seats,
        ticket_price=event.ticket_price,
        organizer_id=current_user.id,
        status="published"
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# PUBLIC_INTERFACE
@router.get("/events/", response_model=List[EventOut], tags=["events"], summary="List/search events")
def list_events(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Search by title or desc"),
    status_filter: Optional[str] = Query("published"),
    skip: int = 0,
    limit: int = 20,
):
    query = db.query(Event)
    if q:
        query = query.filter(Event.title.ilike(f"%{q}%") | Event.description.ilike(f"%{q}%"))
    if status_filter:
        query = query.filter(Event.status == status_filter)
    return query.offset(skip).limit(limit).all()

# PUBLIC_INTERFACE
@router.get("/events/{event_id}", response_model=EventOut, tags=["events"], summary="Get event details")
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).get(event_id)
    if not event:
        raise HTTPException(404, "Event not found")
    return event

# PUBLIC_INTERFACE
@router.put("/events/{event_id}", response_model=EventOut, tags=["events"], summary="Edit event")
def edit_event(event_id: int, event: EventCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_event = db.query(Event).get(event_id)
    if not db_event:
        raise HTTPException(404, "Event not found")
    if not (current_user.is_admin or (current_user.is_organizer and db_event.organizer_id == current_user.id)):
        raise HTTPException(403, "Not authorized")
    for field, value in event.dict().items():
        setattr(db_event, field, value)
    db.commit()
    db.refresh(db_event)
    return db_event

# PUBLIC_INTERFACE
@router.delete("/events/{event_id}", tags=["events"], summary="Delete event")
def delete_event(event_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_event = db.query(Event).get(event_id)
    if not db_event:
        raise HTTPException(404, "Event not found")
    if not (current_user.is_admin or (current_user.is_organizer and db_event.organizer_id == current_user.id)):
        raise HTTPException(403, "Not authorized")
    db.delete(db_event)
    db.commit()
    return {"ok": True}

# ---- BOOKINGS ----

# PUBLIC_INTERFACE
@router.post("/bookings/", response_model=BookingOut, tags=["bookings"], summary="Book tickets for event")
def book_event(booking: BookingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    event = db.query(Event).get(booking.event_id)
    if not event or event.status != "published":
        raise HTTPException(400, "Invalid event")
    if booking.quantity < 1 or booking.quantity > event.available_seats:
        raise HTTPException(400, "Not enough seats available")
    # Decrement inventory
    event.available_seats -= booking.quantity
    total_price = booking.quantity * event.ticket_price
    db_booking = Booking(
        user_id=current_user.id,
        event_id=booking.event_id,
        quantity=booking.quantity,
        total_price=total_price,
        status="pending",
        payment_status="pending"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

# PUBLIC_INTERFACE
@router.post("/bookings/{booking_id}/pay", tags=["bookings"], summary="Mock pay for a booking")
def pay_booking(booking_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    booking = db.query(Booking).get(booking_id)
    if not booking or booking.user_id != current_user.id:
        raise HTTPException(404, "Booking not found")
    if booking.payment_status == "paid":
        return {"msg": "Already paid", "payment_reference": booking.payment_reference}
    res = process_mock_payment(booking.user_id, booking.total_price)
    booking.payment_status = "paid"
    booking.status = "confirmed"
    booking.payment_reference = res["payment_reference"]
    db.commit()
    send_email_stub(current_user.email, "Booking Confirmed", f"You've successfully booked {booking.quantity} tickets.")
    return {"msg": "Payment successful", "payment_reference": booking.payment_reference}

# PUBLIC_INTERFACE
@router.get("/me/bookings", response_model=List[BookingOut], tags=["bookings"], summary="List my bookings")
def my_bookings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Booking).filter(Booking.user_id == current_user.id).all()

# ---- ADMIN ----

# PUBLIC_INTERFACE
@router.get("/admin/events", response_model=List[EventOut], tags=["admin"], summary="List all events (admin/moderation)")
def admin_events(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(403, "Admin only")
    return db.query(Event).all()

# PUBLIC_INTERFACE
@router.get("/admin/analytics", tags=["admin"], summary="Admin analytics - simple metrics")
def admin_analytics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(403, "Admin only")
    event_count = db.query(Event).count()
    user_count = db.query(User).count()
    booking_count = db.query(Booking).count()
    revenue = db.query(Booking).filter(Booking.payment_status == "paid").with_entities(
        Booking.total_price
    )
    total_revenue = sum([b.total_price for b in revenue])
    return {
        "events": event_count,
        "users": user_count,
        "bookings": booking_count,
        "revenue": total_revenue,
    }

# ---- NOTIFICATIONS (webhook STUBS) ----

@router.post("/notify/email", tags=["notify"], summary="Webhook to trigger email")
def webhook_email(to: str, subject: str, body: str):
    send_email_stub(to, subject, body)
    return {"msg": "Email sent (stub)"}
