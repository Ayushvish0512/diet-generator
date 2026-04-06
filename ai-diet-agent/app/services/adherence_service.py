from app.db.supabase_client import supabase

def log_adherence(meal_name: str, followed: bool, feedback: str = None):
    supabase.table("meal_history") \
        .update({
            "followed": followed,
            "feedback_notes": feedback
        }) \
        .eq("meal_name", meal_name) \
        .execute()

    return {"status": "updated"}
