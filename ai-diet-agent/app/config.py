import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    HF_TOKEN: str = os.getenv("HF_TOKEN")
    USE_LOCAL_MODEL: bool = os.getenv("USE_LOCAL_MODEL", "false").lower() == "true"
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "MedAIBase/MedGemma1.5:4b-it")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()

