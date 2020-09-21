from fastapi.testclient import TestClient
from main import app
from main import Task
import uuid
import json

client = TestClient(app)

def test_read_main_returns_not_found():
 response = client.get('/')
 assert response.status_code == 404
 assert response.json() == {'detail': 'Not Found'}

def test_get_all_notes():
    response = client.get('/task')
    assert response.status_code == 200

def test_create_note_ok():
    # Should return 200 due to correct payload
    data = json.dumps(
        {"description": "test_one", "completed": "false"}
    )
    response = client.post(
        "/task",
        data
    )
    print(response.json())
    assert response.status_code == 200

def test_create_note_not_ok():
    # Should return 422 due to incorrect payload
    data = json.dumps(
    {"incorrect": "payload", "test": "false"}
    )
    response = client.post(
        "/task", data)
    assert response.status_code == 422

