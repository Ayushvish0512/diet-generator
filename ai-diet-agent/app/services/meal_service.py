from app.db.supabase_client import get_supabase
from app.models.user import UserPreferences
from app.models.meal import MealPlan
from app.services.ai_service import generate_meal_plan

async def create_or_update_preferences(user_id: str, preferences: UserPreferences):
    supabase = await get_supabase()
    data = {**preferences.dict(), "user_id": user_id}
    await supabase.table("user_preferences").upsert(data).execute()

async def generate_and_save_meal(user_id: str) -> MealPlan:
    supabase = await get_supabase()
    
    # Fetch preferences
    resp = await supabase.table("user_preferences").select("*").eq("user_id", user_id).execute()
    if not resp.data:
        raise ValueError("No preferences found for user")
    
    prefs = UserPreferences(**resp.data[0])
    meal_plan = await generate_meal_plan(prefs)
    
    # Save meal plan
    await supabase.table("meal_plans").insert({
        "user_id": user_id,
        "date": meal_plan.date.isoformat(),
        "plan_data": meal_plan.model_dump_json()
    }).execute()
    
    return meal_plan

