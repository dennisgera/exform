from app.controllers.video import VideoController
from app.repositories.user import UserRepository
from app.repositories.video import VideoRepository
from app.services.user import UserService
from app.services.video import VideoService
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.controllers.user import UserController
from app.schemas.token import TokenPayload
from app.schemas.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_user_controller(db: AsyncSession = Depends(get_db)) -> UserController:
    repository = UserRepository(db)
    service = UserService(repository)
    return UserController(service)

def get_video_controller(db: AsyncSession = Depends(get_db)) -> VideoController:
    repository = VideoRepository(db)
    service = VideoService(repository)
    return VideoController(service)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_controller: UserController = Depends(get_user_controller)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if not token_data.sub:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_controller.get_by_id(id=int(token_data.sub))
    if not user:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
    user_controller: UserController = Depends(get_user_controller)
) -> User:
    if not await user_controller.service.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
