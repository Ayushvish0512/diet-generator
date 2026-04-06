from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.db.supabase_client import get_supabase

security = HTTPBearer()

async def get_current_user_id(token: Annotated[str, Depends(security)]):
    # Simplified auth - replace with proper JWT validation
    # In production: decode JWT from Supabase/R Auth
    if token != "Bearer valid-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return "user-123"  # Replace with decoded user ID

async def get_db():
    return await get_supabase()

