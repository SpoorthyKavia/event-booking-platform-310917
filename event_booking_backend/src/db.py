"""
Database setup using SQLAlchemy and PostgreSQL.

Reads DB config from environment variables:
- POSTGRES_URL
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- POSTGRES_PORT
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ.get("POSTGRES_URL")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_PORT = os.environ.get("POSTGRES_PORT", 5432)

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# PUBLIC_INTERFACE
def get_db():
    """Yield a SQLAlchemy DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
