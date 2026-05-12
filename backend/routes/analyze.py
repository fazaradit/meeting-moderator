from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.llm_service import analyze_transcript

router = APIRouter()

class TranscriptInput(BaseModel):
    transkrip: str

@router.post("/analyze")
async def analyze(data: TranscriptInput):
    if len(data.transkrip.strip()) < 20:
        raise HTTPException(400, "Transkrip terlalu pendek")
    
    try:
        result = analyze_transcript(data.transkrip)
        return {
            "status": "sukses",
            "analisis": result
        }
    except Exception as e:
        raise HTTPException(500, f"Error analisis: {str(e)}")