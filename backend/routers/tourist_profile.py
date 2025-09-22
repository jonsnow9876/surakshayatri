import hashlib
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Tourist

router = APIRouter()


# ---------- Helper: Hash password ----------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ---------- Login tourist by passport + password or permanent ID ----------
@router.get("/login", summary="Login tourist by passport and password")
def login_tourist(
    passport: Optional[str] = Query(None),
    password: Optional[str] = Query(None),
    tourist_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Login tourist using either passport number + password, or tourist_id.
    Returns full profile including temp_id for local storage.
    """
    if not ((passport and password) or tourist_id):
        raise HTTPException(status_code=400, detail="Provide passport + password or tourist_id")
    
    query = db.query(Tourist)
    
    if passport and password:
        passport_clean = passport.strip().upper()
        tourist = query.filter(func.upper(func.trim(Tourist.passport)) == passport_clean).first()
        if not tourist:
            raise HTTPException(status_code=404, detail="Tourist not found")

        # Compare hashed password
        if not tourist.password:
            raise HTTPException(status_code=400, detail="Password not set for this tourist")

        if tourist.password != hash_password(password):
            raise HTTPException(status_code=401, detail="Invalid password")
    elif tourist_id:
        tourist_id_clean = tourist_id.strip()
        tourist = query.filter(Tourist.id == tourist_id_clean).first()
        if not tourist:
            raise HTTPException(status_code=404, detail="Tourist not found")
    else:
        raise HTTPException(status_code=400, detail="Invalid login parameters")
    
    return {
        "id": tourist.id,
        "temp_id": tourist.temp_id,
        "name": tourist.name,
        "passport": tourist.passport,
        "itinerary": tourist.itinerary,
        "phone": getattr(tourist, "phone", None),
        "resolved": getattr(tourist, "resolved", None)
    }


# ---------- Fetch tourist profile by permanent ID ----------
@router.get("/{tourist_id}", summary="Get tourist profile by ID")
def get_tourist_profile(
    tourist_id: str,
    db: Session = Depends(get_db)
):
    """
    Get tourist profile by permanent ID.
    Returns: name, passport, temp_id, itinerary, phone, resolved
    """
    tourist = db.query(Tourist).filter(Tourist.id == tourist_id).first()
    if not tourist:
        raise HTTPException(status_code=404, detail="Tourist not found")
    
    return {
        "id": tourist.id,
        "temp_id": tourist.temp_id,
        "name": tourist.name,
        "passport": tourist.passport,
        "itinerary": tourist.itinerary,
        "phone": getattr(tourist, "phone", None),
        "resolved": getattr(tourist, "resolved", None)
    }
