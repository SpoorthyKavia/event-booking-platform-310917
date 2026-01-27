from src.models import User, Event
from src.schemas import UserCreate, UserOut, EventCreate, EventOut
from datetime import datetime

def test_user_schema_validation():
    user = UserCreate(email="foo@bar.com", password="abc123", full_name="F U")
    assert user.email == "foo@bar.com"
    out = UserOut(
        id=1,
        email="foo@bar.com",
        full_name="F U",
        is_active=True,
        is_organizer=False,
        is_admin=False,
        created_at=datetime.utcnow()
    )
    assert out.dict()["email"] == "foo@bar.com"

def test_event_schema_validation():
    now = datetime.utcnow()
    event = EventCreate(
        title="T",
        description="desc",
        location="loc",
        start_time=now,
        end_time=now,
        total_seats=10,
        ticket_price=19.99
    )
    assert event.title == "T"
    out = EventOut(
        id=2, title="A", description="dd", location="loc", start_time=now, end_time=now,
        total_seats=50, available_seats=50, ticket_price=29.5, organizer_id=1,
        status="published", created_at=now
    )
    assert out.id == 2
