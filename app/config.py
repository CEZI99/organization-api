import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings:
    # Обязательные параметры
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    API_KEY: str = os.getenv("API_KEY")

    # Опциональные параметры с дефолтными значениями
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    APP_ENV: str = os.getenv("APP_ENV", "production")

    # Валидация обязательных параметров
    def __init__(self):
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL не задан в .env файле")
        if not self.API_KEY:
            raise ValueError("API_KEY не задан в .env файле")

settings = Settings()