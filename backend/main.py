from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.transcribe import router as transcribe_router
from backend.routes.analyze import router as analyze_router
from backend.routes.history import router as history_router
from backend.models.database import init_db

app = FastAPI(title="Meeting Moderator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(transcribe_router, prefix="/api", tags=["Transkripsi"])
app.include_router(analyze_router, prefix="/api", tags=["Analisis"])
app.include_router(history_router, prefix="/api", tags=["History"])

@app.get("/")
def root():
    return {"status": "Meeting Moderator API berjalan"}