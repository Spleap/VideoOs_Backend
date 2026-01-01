from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "VideoOs Backend"
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # DMXAPI Configuration
    DMXAPI_KEY: str
    DMXAPI_BASE_URL: str = "https://www.dmxapi.cn/v1"
    DMXAPI_GEMINI_BASE_URL: str = "https://www.dmxapi.cn/v1beta"

    class Config:
        env_file = ".env"

settings = Settings()
