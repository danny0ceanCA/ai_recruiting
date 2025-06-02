"""CRUD operations."""
from sqlalchemy.orm import Session

from app.models import models
from app import schemas


def get_students(db: Session):
    return db.query(models.Student).all()


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_jobs(db: Session):
    return db.query(models.Job).all()


def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
