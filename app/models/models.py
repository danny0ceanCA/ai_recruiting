"""SQLAlchemy models."""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, index=True)
    name = Column(String, nullable=False)
    background = Column(Text)
    education = Column(Text)
    experience = Column(Text)
    qualities = Column(Text)
    embedding = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    matches = relationship("Match", back_populates="student")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    matches = relationship("Match", back_populates="job")

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    score = Column(Float)
    finalized = Column(Integer, default=0)
    archived = Column(Integer, default=0)

    student = relationship("Student", back_populates="matches")
    job = relationship("Job", back_populates="matches")
