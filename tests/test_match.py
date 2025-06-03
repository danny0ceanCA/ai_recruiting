import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import database
from app.models import models
from app.services import match

@pytest.fixture
def db():
    database.init()
    database.Base.metadata.drop_all(bind=database.engine)
    database.Base.metadata.create_all(bind=database.engine)
    session = database.SessionLocal()
    try:
        yield session
    finally:
        session.close()
        database.Base.metadata.drop_all(bind=database.engine)


def test_match_job_to_students(db, monkeypatch):
    s1 = models.Student(name="Alice", embedding="1 0 0")
    s2 = models.Student(name="Bob", embedding="0 1 0")
    db.add_all([s1, s2])
    job = models.Job(title="Engineer", description="something")
    db.add(job)
    db.commit()
    monkeypatch.setattr(match, "embed_text", lambda text: [1.0, 0.0, 0.0])
    result = match.match_job_to_students(db, job, top_k=2)
    assert [s.name for s in result] == ["Alice", "Bob"]
