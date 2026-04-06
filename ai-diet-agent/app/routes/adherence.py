from fastapi import APIRouter, Depends
from typing import Optional
from app.services.adherence_service import log_adherence
from app.dependencies import get_current_user_id

router = APIRouter()

@router.post("/log-adherence")
def log_adherence_endpoint(meal_name: str, followed: bool, feedback: Optional[str] = None, user_id: str = Depends(get_current_user_id)):
    result = log_adherence(meal_name, followed, feedback)
    return result
