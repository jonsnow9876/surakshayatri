from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean, Float, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import uuid
import enum

# ==========================
# Enum for Management User Roles
# ==========================

class ManagerStatus(enum.Enum):
    admin = "admin"
    manager = "manager"
    staff = "staff"

# ==========================
# Tourist Model
# ==========================

class Tourist(Base):
    __tablename__ = "tourists"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    passport = Column(String, unique=True, nullable=False)
    temp_id = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)

    itinerary = Column(String, nullable=True)
    phone = Column(String, nullable=False)

    blockchain_hash = Column(String, nullable=True)
    resolved = Column(Boolean, default=False, nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    radius = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    reports = relationship("Report", back_populates="tourist", cascade="all, delete-orphan")


# ==========================
# History Model
# ==========================

class History(Base):
    __tablename__ = "history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    tourist_id = Column(String, nullable=False)
    temp_id = Column(String, nullable=False)
    itinerary = Column(String, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ==========================
# AlertStatus Model
# ==========================

class AlertStatus(Base):
    __tablename__ = "alert_status"

    alert_uuid = Column(String, primary_key=True)
    resolved = Column(Boolean, default=False, nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(String, nullable=True)
    last_block_hash = Column(String, nullable=True)


# ==========================
# Reports Model
# ==========================

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    tourist_id = Column(String, ForeignKey("tourists.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tourist = relationship("Tourist", back_populates="reports")


# ==========================
# Management Users Model
# ==========================

class ManagementUser(Base):
    __tablename__ = "management_users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Enum(ManagerStatus), nullable=False, default=ManagerStatus.manager)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
