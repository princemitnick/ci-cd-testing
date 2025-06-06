from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_task():
    task = {"id": 99, "title": "Mission DevOps", "completed": False}
    response = client.post("/tasks/", json=task)
    assert response.status_code == 200
    assert response.json()["title"] == "Mission DevOps"