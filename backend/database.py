from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------
# Database URL
# ------------------------
DATABASE_URL = "sqlite:///./data/app.db"

# ------------------------
# Engine
# ------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite with threads
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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
