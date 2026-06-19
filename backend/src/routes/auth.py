from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from src.config import Settings, get_settings
from src.models.UserDataModel import UserDataModel
from src.routes.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UpdateUserRequest,
    UserResponse,
)
from src.utils.auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from src.models import AuthEnum

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def _clean_user_response(user: dict) -> dict:
    if not user:
        return None
    user = user.copy()
    user.pop("hashed_password", None)
    return user


def _get_bearer_token(request: Request) -> str:
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthEnum.AUTH_HEADER_MISSED.value,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authorization.split(" ", 1)[1]


def _get_current_user(request: Request, app_settings: Settings = Depends(get_settings)) -> dict:
    token = _get_bearer_token(request)
    payload = decode_access_token(token, app_settings)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthEnum.TOKEN_PAYLOAD_MISSED_USER_ID.value,
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_model = UserDataModel(request.app.state.db_client)
    current_user = user_model.get_user_by_id(user_id)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthEnum.USER_NOT_FOUND.value,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


@auth_router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request_body: RegisterRequest,
    request: Request,
    app_settings: Settings = Depends(get_settings),
):
    user_model = UserDataModel(request.app.state.db_client)

    if user_model.get_user_by_email(request_body.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=AuthEnum.USER_WITH_EMAIL_ALREADY_EXITS.value,
        )

    if user_model.get_user_by_username(request_body.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=AuthEnum.USER_WITH_NAME_ALREADY_EXITS.value,
        )

    hashed_password = hash_password(request_body.password)
    new_user = {
        "username": request_body.username,
        "email": request_body.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "updated_at": None,
    }
    saved_user = user_model.create_user(new_user)
    token = create_access_token(
        {"user_id": saved_user["_id"], "email": saved_user["email"]},
        app_settings,
    )
    return {
        "access_token": token,
        "token_type": "Bearer",
        "user": _clean_user_response(saved_user),
    }


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    request_body: LoginRequest,
    request: Request,
    app_settings: Settings = Depends(get_settings),
):
    user_model = UserDataModel(request.app.state.db_client)
    stored_user = user_model.get_user_by_email(request_body.email)

    if stored_user is None or not verify_password(request_body.password, stored_user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthEnum.INVALID_EMAIL_OR_PASSWORD.value,
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        {"user_id": stored_user["_id"], "email": stored_user["email"]},
        app_settings,
    )
    return {
        "access_token": token,
        "token_type": "Bearer",
        "user": _clean_user_response(stored_user),
    }


@auth_router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(_get_current_user)):
    return _clean_user_response(current_user)


@auth_router.put("/profile", response_model=UserResponse)
async def update_profile(
    request_body: UpdateUserRequest,
    current_user: dict = Depends(_get_current_user),
    request: Request = None,
):
    if not any([request_body.username, request_body.email, request_body.password]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=AuthEnum.AT_LEAST_ONE_FIELD_MUST_BE_PROVIDED.value,
        )

    user_model = UserDataModel(request.app.state.db_client)
    updates = {}

    if request_body.username and request_body.username != current_user.get("username"):
        existing = user_model.get_user_by_username(request_body.username)
        if existing and existing.get("_id") != current_user.get("_id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthEnum.USERNAME_ALREADY_IN_USE.value,
            )
        updates["username"] = request_body.username

    if request_body.email and request_body.email != current_user.get("email"):
        existing = user_model.get_user_by_email(request_body.email)
        if existing and existing.get("_id") != current_user.get("_id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthEnum.EMAIL_ALREADY_IN_USE.value,
            )
        updates["email"] = request_body.email

    if request_body.password:
        updates["hashed_password"] = hash_password(request_body.password)

    if updates:
        updates["updated_at"] = datetime.utcnow()
        updated_user = user_model.update_user(current_user.get("_id"), updates)
        if updated_user is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=AuthEnum.FAILED_TO_UPDATE.value,
            )
        return _clean_user_response(updated_user)

    return _clean_user_response(current_user)


@auth_router.delete("/profile", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    current_user: dict = Depends(_get_current_user),
    request: Request = None,
):
    user_model = UserDataModel(request.app.state.db_client)
    success = user_model.delete_user(current_user.get("_id"))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AuthEnum.FAILED_TO_DELETE_USER.value,
        )
    return None
