from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.transcribe import router as transcribe_router
from backend.routes.analyze import router as analyze_router

app = FastAPI(title="Meeting Moderator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcribe_router, prefix="/api", tags=["Transkripsi"])
app.include_router(analyze_router, prefix="/api", tags=["Analisis"])

@app.get("/")
def root():
    return {"status": "Meeting Moderator API berjalan"}