from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ==========================
# Tourist Registration
# ==========================
class TouristRegisterRequest(BaseModel):
    name: str
    email: str
    phone: str
    passport: str
    password: str
    itinerary: Optional[str] = None


class TouristRegisterResponse(BaseModel):
    tourist_id: str
    temp_id: str
    qr_code_base64: str


# ==========================
# Itinerary Update
# ==========================
class UpdateItineraryRequest(BaseModel):
    tourist_id: str
    itinerary: str


# ==========================
# Panic & Alerts
# ==========================
class PanicRequest(BaseModel):
    tourist_id: str
    lat: float
    lon: float
    message: Optional[str] = None


class PanicResponse(BaseModel):
    alert_uuid: str
    temp_id: str
    lat: float
    lon: float
    timestamp: datetime
    blockchain_hash: str
    message: Optional[str] = None


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


# ==========================
# Unified Panic + Report
# ==========================
class PanicReportRequest(BaseModel):
    tourist_id: str
    lat: float
    lon: float
    message: Optional[str] = None
    sos: bool = False
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None  # base64 string


class PanicReportResponse(BaseModel):
    alert_uuid: str
    temp_id: str
    lat: float
    lon: float
    timestamp: str
    blockchain_hash: str


# ==========================
# GeoFence Zones
# ==========================
class ZoneResponse(BaseModel):
    id: str
    name: str
    lat: float
    lon: float
    radius: float

    # Pydantic v2 replacement for orm_mode
    model_config = {
        "from_attributes": True
    }
