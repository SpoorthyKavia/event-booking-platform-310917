# Backend Test Suite

- Run local: `pytest`
- Uses SQLite database in tests (fresh per session, no impact on dev/prod).
- Add more tests in this folder to cover the FastAPI API, models, and schemas.

Structure:
- `conftest.py` - DB setup and app client
- `test_api_main.py` - API endpoint tests for health+auth example
- `factories.py` - For user/event/booking creation in DB during tests
