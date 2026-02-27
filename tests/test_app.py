import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)

def setup_function():
    # Reset activities to initial state before each test
    for activity in activities.values():
        activity['participants'].clear()

def test_get_activities():
    # Arrange: (nothing to arrange, just ensure clean state)
    setup_function()
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all('description' in v for v in data.values())
    assert all('participants' in v for v in data.values())

def test_signup_success():
    setup_function()
    email = "student1@mergington.edu"
    activity = list(activities.keys())[0]
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]['participants']
    assert "message" in response.json()

def test_signup_already_registered():
    setup_function()
    email = "student2@mergington.edu"
    activity = list(activities.keys())[0]
    # Arrange
    activities[activity]['participants'].append(email)
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")

def test_signup_activity_not_found():
    setup_function()
    email = "student3@mergington.edu"
    # Act
    response = client.post(f"/activities/NonexistentActivity/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json().get("detail", "")
