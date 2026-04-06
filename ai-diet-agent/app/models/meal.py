from app.db.supabase_client import supabase
from app.utils.prompt_builder import build_prompt
from app.services.ai_service import generate_meal_from_ai
from datetime import date

def generate_meal(user_id: str):
    # Fetch preferences
    pref_res = supabase.table("users").select("*").eq("id", user_id).execute()
    preferences = pref_res.data[0]

    # Fetch failed meals
    history_res = supabase.table("diet_history") \
        .select("*") \
        .eq("user_id", user_id) \
        .eq("followed", False) \
        .execute()

    failed_meals = [h["meal_name"] for h in history_res.data]
    feedback_notes = [h["feedback_notes"] for h in history_res.data if h["feedback_notes"]]

    # Build prompt
    prompt = build_prompt(preferences, failed_meals, feedback_notes)

    # Call AI
    meal = generate_meal_from_ai(prompt)

    # Save to history
    supabase.table("diet_history").insert({
        "user_id": user_id,
        "meal_name": meal["name"],
        "date_assigned": str(date.today()),
        "followed": None
    }).execute()

    return meal