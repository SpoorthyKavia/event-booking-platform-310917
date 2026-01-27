"""
Pydantic schemas for Event Booking API.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    full_name: Optional[str]

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    full_name: Optional[str]
    is_active: bool
    is_organizer: bool
    is_admin: bool
    created_at: datetime

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    title: str
    description: Optional[str]
    location: Optional[str]
    start_time: datetime
    end_time: datetime
    total_seats: int
    ticket_price: float

class EventCreate(EventBase):
    pass

class EventOut(EventBase):
    id: int
    available_seats: int
    organizer_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    event_id: int
    quantity: int

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int
    user_id: int
    total_price: float
    booking_time: datetime
    status: str
    payment_status: str

    class Config:
        orm_mode = True
