import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_database_status():
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json() == {"estado": "Base de datos conectada"}
