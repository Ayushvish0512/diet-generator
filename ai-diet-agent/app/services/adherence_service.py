from app.db.supabase_client import get_supabase
from app.models.history import AdherenceLog

async def log_adherence(log: AdherenceLog):
    supabase = await get_supabase()
    data = log.dict()
    await supabase.table("adherence_logs").insert(data).execute()

