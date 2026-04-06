from fastapi import APIRouter, Depends
from app.models.history import AdherenceLog
from app.services.adherence_service import log_adherence

router = APIRouter()

@router.post("/log-adherence")
async def log_adherence_endpoint(log: AdherenceLog):
    await log_adherence(log)
    return {"message": "Adherence logged"}

