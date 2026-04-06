from fastapi import APIRouter, Depends
from app.models.meal import MealPlan
from app.services.meal_service import generate_and_save_meal
from app.dependencies import get_current_user_id

router = APIRouter()

@router.post("/generate-meal", response_model=MealPlan)
async def generate_meal(user_id: str = Depends(get_current_user_id)):
    meal_plan = await generate_and_save_meal(user_id)
    return meal_plan

