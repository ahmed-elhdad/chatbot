from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    GOOGLE_API_KEY: Optional[str] = None

    MONGODB_USERNAME: Optional[str] = None
    MONGODB_PASSWORD: Optional[str] = None
    MONGODB_URI: Optional[str] = None
    
    FILE_ALLOWED_TYPES:List
    FILE_MAX_SIZE:int
    FILE_ALLOWED_TYPES: List[str]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str 
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


def get_settings():
    return Settings()