from fastapi import APIRouter, Depends
from app.services.meal_service import generate_meal
from app.dependencies import get_current_user_id

router = APIRouter()

@router.post("/generate-meal")
def generate_meal_endpoint(user_id: str = Depends(get_current_user_id)):
    meal = generate_meal(user_id)
    return meal
