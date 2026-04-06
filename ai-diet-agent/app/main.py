from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import preferences, meals, adherence
from app.dependencies import lifespan

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup and shutdown logic here if needed
    yield

app = FastAPI(
    title="AI Diet Agent",
    description="AI-powered personalized diet generator",
    lifespan=lifespan
)

app.include_router(preferences.router, prefix="/preferences", tags=["preferences"])
app.include_router(meals.router, prefix="/meals", tags=["meals"])
app.include_router(adherence.router, prefix="/adherence", tags=["adherence"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

