from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --------------------------
# Tourist Registration
# --------------------------

class TouristRegisterRequest(BaseModel):
    name: str
    passport: str
    itinerary: Optional[str] = None
    emergency_contact: str

class TouristRegisterResponse(BaseModel):
    tourist_id: str       # permanent UUID
    temp_id: str          # temporary anonymized ID
    qr_code_base64: str   # QR code for temp_id

# ---------- Schema for updating itinerary ----------
class UpdateItineraryRequest(BaseModel):
    tourist_id: str
    itinerary: str

# --------------------------
# Panic Alert
# --------------------------

class PanicRequest(BaseModel):
    tourist_id: str  # permanent tourist ID
    lat: float
    lon: float
    message: str | None = None

class PanicResponse(BaseModel):
    alert_uuid: str
    temp_id: str
    lat: float
    lon: float
    timestamp: datetime
    blockchain_hash: str
    message: Optional[str] = None

# --------------------------
# Alert Status
# --------------------------

class AlertStatusResponse(BaseModel):
    alert_uuid: str
    temp_id: str
    lat: float
    lon: float
    timestamp: datetime
    blockchain_hash: str
    resolved: bool
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    message: Optional[str] = None
