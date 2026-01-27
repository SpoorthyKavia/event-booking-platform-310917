# Backend Test Suite

## How to Run Backend Tests

1. Install dependencies  
   ```
   pip install -r requirements.txt
   pip install -r requirements-test.txt
   ```

2. Run tests  
   ```
   pytest
   ```

- Database: Tests use SQLite in-memory or local test DB (see conftest.py), so no dev/prod DB is touched.
- Structure:
  - `conftest.py` – test DB/session setup and FastAPI app client fixture (overrides normal DB).
  - `test_api_main.py` – core API endpoint test coverage (health & auth flows).
  - `test_models_schemas.py` – model/schema validation tests.
  - `factories.py` – helpers for test data creation.
- Add more tests in this folder for FastAPI API, models, schemas, and background logic.
