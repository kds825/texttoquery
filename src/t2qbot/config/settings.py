from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str
    db_url: str
    llm_provider: str
    ollama_base_url: str
    ollama_model: str
    
    openai_api_key: str
    openai_model: str
    max_rows: int
    default_limit: int
    allow_tables: str
    
    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()