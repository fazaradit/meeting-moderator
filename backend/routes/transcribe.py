import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.services.stt_service import transcribe_audio

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    allowed = [".mp3", ".wav", ".m4a", ".ogg", ".webm"]
    ext = os.path.splitext(file.filename)[1].lower()
    
    if ext not in allowed:
        raise HTTPException(400, f"Format tidak didukung. Gunakan: {allowed}")
    
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    try:
        result = transcribe_audio(file_path)
        return {
            "status": "sukses",
            "filename": file.filename,
            "transkrip": result["text"],
            "durasi_detik": result["duration"]
        }
    except Exception as e:
        raise HTTPException(500, f"Error transkripsi: {str(e)}")