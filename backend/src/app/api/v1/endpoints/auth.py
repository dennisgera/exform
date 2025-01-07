from datetime import timedelta
from typing import Any
from app.controllers.user import UserController
from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.deps import get_current_active_user, get_user_controller
from fastapi.security import OAuth2PasswordRequestForm
from app.core import security
from app.core.config import settings
from app.schemas.token import Token
from app.schemas.user import User, UserCreate

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_controller: UserController = Depends(get_user_controller),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_controller.authenticate(
        email=form_data.username, password=form_data.password
    )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )


@router.post("/register", response_model=User)
async def register(
    *,
    user_in: UserCreate,
    user_controller: UserController = Depends(get_user_controller),
) -> Any:
    """
    Create new user.
    """
    user = await user_controller.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists.",
        )
    user = await user_controller.create(user_in)
    return user


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
