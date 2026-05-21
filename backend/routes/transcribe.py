import os
import json
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.services.stt_service import transcribe_audio
from backend.services.llm_service import analyze_transcript
from backend.models.database import get_db, MeetingResult

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...), db: Session = Depends(get_db)):
    allowed = [".mp3", ".wav", ".m4a", ".ogg", ".webm"]
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed:
        raise HTTPException(400, f"Format tidak didukung. Gunakan: {allowed}")

    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        stt_result = transcribe_audio(file_path)
        transkrip = stt_result["text"]
        durasi = stt_result["duration"]

        analisis = analyze_transcript(transkrip)

        # Simpan ke database
        record = MeetingResult(
            filename=file.filename,
            durasi_detik=str(durasi),
            transkrip=transkrip,
            analisis_json=json.dumps(analisis, ensure_ascii=False)
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "status": "sukses",
            "id": record.id,
            "filename": file.filename,
            "durasi_detik": durasi,
            "transkrip": transkrip,
            "analisis": analisis
        }

    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")