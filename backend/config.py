import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://cadastro:senha123@postgres:5432/cadastro_db"
    )
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"

settings = Settings()
