"""Match utilities."""
from sqlalchemy.orm import Session
from app.models import models
from app.services.embeddings import embed_text


def match_job_to_students(db: Session, job: models.Job, top_k: int = 5) -> list[models.Student]:
    job_vec = embed_text(job.description or job.title)
    # naive implementation: compute distance to all student embeddings
    students = db.query(models.Student).all()
    scored = []
    for s in students:
        if not s.embedding:
            continue
        # compute dummy similarity: dot product
        score = sum(float(a) * float(b) for a, b in zip(job_vec, map(float, s.embedding.split())))
        scored.append((score, s))
    scored.sort(reverse=True, key=lambda t: t[0])
    return [s for _, s in scored[:top_k]]
