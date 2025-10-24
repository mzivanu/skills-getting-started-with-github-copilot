def test_root_redirect():
    response = client.get("/")
    # FastAPI RedirectResponse geeft status 200 in TestClient, maar bevat een redirect-url
    assert response.status_code in (200, 307)
    assert str(response.url).endswith("/static/index.html")
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    response = client.post("/activities/Chess Club/signup?email=" + email)
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Double signup should fail
    response2 = client.post("/activities/Chess Club/signup?email=" + email)
    assert response2.status_code == 400

def test_unregister_from_activity():
    email = "testuser@mergington.edu"
    # Unregister should succeed
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 200
    assert "removed" in response.json()["message"]
    # Unregister again should fail
    response2 = client.post(f"/activities/Chess Club/unregister?email={email}")
    assert response2.status_code == 400

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404

def test_unregister_invalid_activity():
    response = client.post("/activities/Nonexistent/unregister?email=someone@mergington.edu")
    assert response.status_code == 404
