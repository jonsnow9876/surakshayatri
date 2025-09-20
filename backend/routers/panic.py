from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PanicRequest
from database import get_db
from models import Tourist
from blockchain import add_block
from datetime import datetime, timezone
import uuid, traceback

router = APIRouter()


@router.post("/", summary="Trigger panic alert")
def trigger_panic(request: PanicRequest, db: Session = Depends(get_db)):
    """
    Trigger a panic alert for a tourist.
    The tourist is identified by their permanent ID.
    The alert is linked to the tourist's current temp_id for anonymity.
    """
    try:
        # Fetch tourist by permanent ID
        tourist = db.query(Tourist).filter(Tourist.id == request.tourist_id).first()
        if not tourist:
            raise HTTPException(status_code=404, detail="Tourist not found")

        # Use current temp_id for anonymity
        temp_id = tourist.temp_id

        # Create alert payload for blockchain
        alert_data = {
            "temp_id": temp_id,
            "lat": request.lat,
            "lon": request.lon,
            "message": request.message,
            "alert_uuid": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        # Add block to blockchain
        block = add_block(alert_data)

        return {
            "alert_uuid": alert_data["alert_uuid"],
            "temp_id": temp_id,
            "lat": request.lat,
            "lon": request.lon,
            "timestamp": alert_data["timestamp"],
            "blockchain_hash": block["hash"]
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
