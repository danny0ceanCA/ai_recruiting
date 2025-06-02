"""Pydantic schemas."""
from pydantic import BaseModel
from datetime import datetime

class StudentBase(BaseModel):
    name: str
    school_id: int | None = None
    background: str | None = None
    education: str | None = None
    experience: str | None = None
    qualities: str | None = None

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    embedding: str | None = None
    created_at: datetime | None = None

    class Config:
        orm_mode = True

class JobBase(BaseModel):
    title: str
    description: str | None = None

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    created_at: datetime | None = None

    class Config:
        orm_mode = True
