from fastapi import APIRouter
from app.db.supabase_client import supabase
from app.models.user import UserPreferences

router = APIRouter()

@router.get("/preferences/{user_id}")
def get_preferences(user_id: str):
    res = supabase.table("preferences") \
        .select("*") \
        .eq("user_id", user_id) \
        .execute()

    return res.data

@router.put("/preferences/{user_id}")
def update_preferences(user_id: str, prefs: UserPreferences):
    supabase.table("preferences") \
        .upsert({
            "user_id": user_id,
            **prefs.dict()
        }) \
        .execute()

    return {"status": "updated"}
