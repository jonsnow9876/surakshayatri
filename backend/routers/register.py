from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Tourist
from schemas import TouristRegisterRequest, TouristRegisterResponse, UpdateItineraryRequest
from pydantic import BaseModel
import uuid, qrcode, base64
from io import BytesIO
import traceback

router = APIRouter()

# ---------- Helper: Generate QR code from tourist ID ----------
def generate_qr_code(tourist_id: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(tourist_id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").get_image()
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


# -------------------------------
# Route 1: Register a New Tourist
# -------------------------------
@router.post("/new", response_model=TouristRegisterResponse)
def register_new_tourist(request: TouristRegisterRequest, db: Session = Depends(get_db)):
    try:
        # Check if passport already exists
        existing = db.query(Tourist).filter(Tourist.passport == request.passport).first()
        if existing:
            raise HTTPException(status_code=400, detail="Passport already registered")

        # Generate IDs
        tourist_id = str(uuid.uuid4())
        temp_id = str(uuid.uuid4())  # temporary anonymized ID

        # Create new Tourist
        tourist = Tourist(
            id=tourist_id,
            name=request.name,
            passport=request.passport,
            temp_id=temp_id,
            itinerary=request.itinerary,
            emergency_contact=request.emergency_contact
        )

        db.add(tourist)
        db.commit()
        db.refresh(tourist)

        qr_code_base64 = generate_qr_code(tourist_id)

        return TouristRegisterResponse(
            tourist_id=tourist_id,
            temp_id=temp_id,
            qr_code_base64=qr_code_base64
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



# -------------------------------
# Route 2: Update Itinerary & Generate New temp_id
# -------------------------------
@router.patch("/update_itinerary", response_model=TouristRegisterResponse)
def update_itinerary(request: UpdateItineraryRequest, db: Session = Depends(get_db)):
    try:
        tourist = db.query(Tourist).filter(Tourist.id == request.tourist_id).first()
        if not tourist:
            raise HTTPException(status_code=404, detail="Tourist not found")

        # Generate new temp_id for anonymity
        new_temp_id = str(uuid.uuid4())
        tourist.temp_id = new_temp_id
        tourist.itinerary = request.itinerary

        db.commit()
        db.refresh(tourist)

        qr_code_base64 = generate_qr_code(tourist.id)

        return TouristRegisterResponse(
            tourist_id=tourist.id,
            temp_id=new_temp_id,
            qr_code_base64=qr_code_base64
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
