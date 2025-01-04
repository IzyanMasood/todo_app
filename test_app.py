import pytest
from fastapi.testclient import TestClient
from main import app
from app import models, schemas
from app.database import SessionLocal, engine

client = TestClient(app)

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def task_id(db_session):
    task_data = {
        "name": "Test Task",
        "description": "This is a test task.",
        "exp_date": "2025-01-01 00:00:00",
        "status": schemas.TaskStatus.PENDING.value
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    task_id = response.json()["id"]

    yield task_id
    client.delete(f"/task/{task_id}")

def test_get_tasks(db_session):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) >= 0

    

def test_get_task(db_session, task_id):
    response = client.get(f"/task/{task_id}")
    assert response.status_code == 200

def test_update_task(db_session, task_id):
    updated_data = {
        "name": "Updated Test Task",
        "description": "Updated description.",
        "exp_date": "2025-02-01 00:00:00",
        "status": schemas.TaskStatus.PENDING.value
    }
    
    response = client.put(f"/task/{task_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]
    assert response.json()["description"] == updated_data["description"]
    assert response.json()["exp_date"] == updated_data["exp_date"]

def test_complete_task(db_session, task_id):
    response = client.patch(f"/task/{task_id}")
    assert response.status_code == 200
    assert response.json()["status"] == schemas.TaskStatus.COMPLETED.value

def test_delete_task(db_session, task_id):
    response = client.delete(f"/task/{task_id}")
    assert response.status_code == 200
