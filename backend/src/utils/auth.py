from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from fastapi import HTTPException, status

from src.config import Settings
from src.models import AuthEnum


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(data: dict, app_settings: Settings, expires_delta: Optional[timedelta] = None) -> str:
    token_data = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=app_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    token_data.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(token_data, app_settings.JWT_SECRET_KEY, algorithm=app_settings.JWT_ALGORITHM)

def decode_access_token(token: str, app_settings: Settings) -> dict:
    try:
        return jwt.decode(token, app_settings.JWT_SECRET_KEY, algorithms=[app_settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthEnum.TOKEN_EXPIRED.value,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthEnum.INVALID_TOKEN.value,
            headers={"WWW-Authenticate": "Bearer"},
        )
