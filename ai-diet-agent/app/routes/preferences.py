from fastapi import APIRouter
from app.db.supabase_client import supabase
from app.models.user import UserPreferences

router = APIRouter()

@router.get("/preferences/{user_id}")
def get_preferences(user_id: str):
    res = supabase.table("users").select("*").eq("id", user_id).execute()
    return res.data

@router.put("/preferences/{user_id}")
def update_preferences(user_id: str, prefs: UserPreferences):
    supabase.table("users") \
        .update(prefs.dict()) \
        .eq("id", user_id) \
        .execute()

    return {"status": "updated"}