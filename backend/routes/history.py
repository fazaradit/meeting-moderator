import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.database import get_db, MeetingResult

router = APIRouter()

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    meetings = db.query(MeetingResult).order_by(
        MeetingResult.created_at.desc()
    ).all()

    return [
        {
            "id": m.id,
            "filename": m.filename,
            "durasi_detik": m.durasi_detik,
            "created_at": m.created_at.strftime("%d %b %Y, %H:%M"),
            "ringkasan": json.loads(m.analisis_json).get("ringkasan", "-")
        }
        for m in meetings
    ]

@router.get("/history/{meeting_id}")
def get_meeting_detail(meeting_id: int, db: Session = Depends(get_db)):
    m = db.query(MeetingResult).filter(MeetingResult.id == meeting_id).first()
    if not m:
        return {"error": "Tidak ditemukan"}
    return {
        "id": m.id,
        "filename": m.filename,
        "durasi_detik": m.durasi_detik,
        "created_at": m.created_at.strftime("%d %b %Y, %H:%M"),
        "transkrip": m.transkrip,
        "analisis": json.loads(m.analisis_json)
    }