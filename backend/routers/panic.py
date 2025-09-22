from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Tourist, Report
from pydantic import BaseModel
from typing import Optional, List
from blockchain import add_block
from datetime import datetime, timezone
import uuid, traceback
from schemas import PanicReportRequest, PanicReportResponse

router = APIRouter()


# ---------- POST /alerts/ ----------
@router.post("/", response_model=PanicReportResponse, summary="Trigger panic/SOS/report alert")
def trigger_alert(request: PanicReportRequest, db: Session = Depends(get_db)):
    try:
        # Fetch tourist by permanent ID
        tourist = db.query(Tourist).filter(Tourist.id == request.tourist_id).first()
        if not tourist:
            raise HTTPException(status_code=404, detail="Tourist not found")
        
        temp_id = tourist.temp_id
        alert_uuid = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        # If report fields are present, save to DB
        if request.title or request.description or request.image:
            new_report = Report(
                tourist_id=request.tourist_id,
                title=request.title or "",
                description=request.description,
                image=request.image
            )
            db.add(new_report)
            db.commit()
            db.refresh(new_report)

        # Prepare blockchain data
        alert_data = {
            "alert_uuid": alert_uuid,
            "temp_id": temp_id,
            "lat": request.lat,
            "lon": request.lon,
            "message": request.message,
            "sos": request.sos,
            "report": {
                "title": request.title,
                "description": request.description,
                "image": request.image
            } if request.title or request.description or request.image else None,
            "timestamp": timestamp
        }

        # Add to blockchain as issue
        block = add_block(alert_data, block_type="issue")

        return {
            "alert_uuid": alert_uuid,
            "temp_id": temp_id,
            "lat": request.lat,
            "lon": request.lon,
            "timestamp": timestamp,
            "blockchain_hash": block["hash"]
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
