from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..db import Base, engine
from .routes import router as api_router
from ..seed import seed_db

app = FastAPI(
    title="Event Booking API",
    description="API for event booking platform with user/auth, events, bookings, payment mock, admin, and notification (stub).",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def create_db_tables_seed():
    """Auto-create DB and seed if empty (dev only)."""
    Base.metadata.create_all(bind=engine)
    from sqlalchemy.orm import Session
    with Session(engine) as db:
        try:
            seed_db(db)
        except Exception as e:
            print("Seed error", e)

app.include_router(api_router)

@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"message": "Healthy"}
