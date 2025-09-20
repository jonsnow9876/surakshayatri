from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import AlertStatus
from blockchain import load_chain, add_block
from datetime import datetime, timezone
from typing import List, Optional, Dict

router = APIRouter()


def _merge_alert_status(chain_alerts: List[Dict], db: Session) -> List[Dict]:
    """
    Merge blockchain alerts with DB resolution status.
    """
    all_status = {s.alert_uuid: s for s in db.query(AlertStatus).all()}
    merged: List[Dict] = []

    for block in chain_alerts:
        data = block.get("data")
        if data is None or data == "genesis":
            continue

        alert_uuid = data.get("alert_uuid")
        status: Optional[AlertStatus] = all_status.get(alert_uuid)

        merged.append({
            "alert_uuid": alert_uuid,
            "temp_id": data.get("temp_id"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "timestamp": block.get("timestamp"),
            "blockchain_index": block.get("index"),
            "blockchain_hash": block.get("hash"),
            "resolved": status.resolved if status else False,
            "resolved_at": status.resolved_at if status else None,
            "resolved_by": status.resolved_by if status else None,
            "message": data.get("message")
        })

    return merged


@router.get("/", summary="Get all alerts")
def get_all_alerts(
    unresolved_only: bool = Query(False, description="Return only unresolved alerts"),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """
    Fetch all alerts from blockchain, optionally filtering unresolved ones.
    """
    chain = load_chain()
    alerts = _merge_alert_status(chain.get("chain", []), db)

    if unresolved_only:
        alerts = [a for a in alerts if not a["resolved"]]

    return alerts


@router.get("/tourist/{temp_id}", summary="Get alerts for a specific tourist temp_id")
def get_alerts_by_tourist(
    temp_id: str,
    unresolved_only: bool = Query(False, description="Return only unresolved alerts"),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """
    Fetch all alerts for a specific tourist temp_id.
    """
    chain = load_chain()
    alerts = _merge_alert_status(chain.get("chain", []), db)
    alerts = [a for a in alerts if a["temp_id"] == temp_id]

    if unresolved_only:
        alerts = [a for a in alerts if not a["resolved"]]

    return alerts


@router.patch("/{alert_uuid}/resolve", summary="Resolve an alert")
def resolve_alert(
    alert_uuid: str,
    resolved_by: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Mark an alert as resolved. Creates a record if missing.
    Also appends a resolution block to the blockchain.
    """
    try:
        now = datetime.now(timezone.utc)

        # --- 1️⃣ Update DB ---
        status: Optional[AlertStatus] = db.query(AlertStatus).filter(
            AlertStatus.alert_uuid == alert_uuid
        ).first()

        if status:
            status.resolved = True
            status.resolved_at = now
            status.resolved_by = resolved_by
        else:
            status = AlertStatus(
                alert_uuid=alert_uuid,
                resolved=True,
                resolved_at=now,
                resolved_by=resolved_by
            )
            db.add(status)

        db.commit()
        db.refresh(status)

        # --- 2️⃣ Append resolution to blockchain ---
        chain = load_chain()

        # Find original alert to get temp_id
        orig_alert = next(
            (b["data"] for b in chain.get("chain", [])
             if isinstance(b.get("data"), dict) and b["data"].get("alert_uuid") == alert_uuid),
            None
        )
        temp_id = orig_alert.get("temp_id") if orig_alert else None

        resolution_data = {
            "alert_uuid": alert_uuid,
            "temp_id": temp_id,
            "resolved": True,
            "resolved_by": resolved_by,
            "resolved_at": now.isoformat()
        }

        new_block = add_block(resolution_data)  # single variable now

        return {
            "alert_uuid": status.alert_uuid,
            "resolved": status.resolved,
            "resolved_at": status.resolved_at,
            "resolved_by": status.resolved_by,
            "blockchain_hash": new_block["hash"],
            "blockchain_index": new_block["index"]
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
