from sqlalchemy import Column, String, DateTime, Boolean, func
from database import Base
from datetime import datetime

# --------------------------
# Tourist Model
# --------------------------
class Tourist(Base):
    __tablename__ = "tourists"

    id = Column(String, primary_key=True, index=True)        # permanent UUID
    name = Column(String, nullable=False)
    passport = Column(String, unique=True, nullable=False)
    temp_id = Column(String, nullable=False)                # temporary anonymized ID for anonymity
    itinerary = Column(String, nullable=True)               # optional itinerary
    emergency_contact = Column(String, nullable=False)
    blockchain_hash = Column(String, nullable=True)         # last blockchain hash
    resolved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)


# --------------------------
# History Model
# --------------------------
class History(Base):
    __tablename__ = "history"

    id = Column(String, primary_key=True, index=True)
    tourist_id = Column(String, nullable=False)
    temp_id = Column(String, nullable=False)               # temporary anonymized ID
    itinerary = Column(String, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# --------------------------
# AlertStatus Model
# --------------------------
class AlertStatus(Base):
    __tablename__ = "alert_status"

    alert_uuid = Column(String, primary_key=True)
    resolved = Column(Boolean, default=False, nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(String, nullable=True)
    last_block_hash = Column(String, nullable=True)        # last block hash for blockchain linkage
