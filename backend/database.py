import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------
# Ensure data folder exists
# ------------------------
os.makedirs("./data", exist_ok=True)

# ------------------------
# Database URL
# ------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")

# ------------------------
# Engine
# ------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# ------------------------
# Session
# ------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ------------------------
# Base class for models
# ------------------------
Base = declarative_base()

# ------------------------
# Dependency for FastAPI
# ------------------------
def get_db():
    """Provide a database session for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()