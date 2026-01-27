import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

# Ensure src/ is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.api.main import app
from src.db import Base, get_db

# Use SQLite for test DB
TEST_DB_URL = "sqlite:///./test_db.sqlite"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency to use test DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Create the tables for a fresh DB every session
    if os.path.exists("test_db.sqlite"):
        os.remove("test_db.sqlite")
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test_db.sqlite"):
        os.remove("test_db.sqlite")


@pytest.fixture()
def client(setup_test_db):
    with TestClient(app) as c:
        yield c
