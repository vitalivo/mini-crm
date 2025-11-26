# src/core/config.py
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    ENVIRONMENT: Literal["dev", "prod", "test"] = "dev"
    
    # База данных
    DATABASE_URL: str = "sqlite:////data/crm.db"
    
    # Для будущих расширений
    PROJECT_NAME: str = "Mini CRM — распределение лидов"
    VERSION: str = "0.1.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()