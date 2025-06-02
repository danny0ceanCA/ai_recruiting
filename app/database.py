"""Database connection utilities."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine
import os

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./test.db"  # fallback for dev
)

engine: Engine | None = None
SessionLocal: sessionmaker | None = None
Base = declarative_base()

def init() -> None:
    global engine, SessionLocal
    if engine is None:
        engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


