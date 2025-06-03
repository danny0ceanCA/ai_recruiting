import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app import database
from app.models import models

@pytest.fixture
def client():
    database.init()
    database.Base.metadata.drop_all(bind=database.engine)
    database.Base.metadata.create_all(bind=database.engine)
    with TestClient(app) as client:
        yield client
    database.Base.metadata.drop_all(bind=database.engine)


def test_create_and_get_student(client):
    resp = client.post("/students", json={"name": "Alice", "school_id": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Alice"
    resp = client.get("/students")
    assert resp.status_code == 200
    students = resp.json()
    assert len(students) == 1
    assert students[0]["name"] == "Alice"


def test_create_and_get_job(client):
    resp = client.post("/jobs", json={"title": "Engineer", "description": "dev"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Engineer"
    resp = client.get("/jobs")
    assert resp.status_code == 200
    jobs = resp.json()
    assert len(jobs) == 1
    assert jobs[0]["title"] == "Engineer"
