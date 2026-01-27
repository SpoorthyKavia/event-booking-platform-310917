def test_health_check(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["message"] == "Healthy"


def test_register_login_flow(client):
    # Register new user
    r = client.post("/auth/register", json={
        "email": "t1@example.com",
        "password": "testpass",
        "full_name": "Test User"
    })
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "t1@example.com"
    assert data["is_active"] is True
    # Duplicate register fails
    r2 = client.post("/auth/register", json={
        "email": "t1@example.com",
        "password": "testpass2",
        "full_name": "Test2"
    })
    assert r2.status_code == 400
    # Login works
    r3 = client.post("/auth/login", json={
        "email": "t1@example.com",
        "password": "testpass"
    })
    assert r3.status_code == 200
    assert "access_token" in r3.json()
    # Login with wrong password fails
    r4 = client.post("/auth/login", json={
        "email": "t1@example.com",
        "password": "wrong"
    })
    assert r4.status_code == 401
