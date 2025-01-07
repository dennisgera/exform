from app.controllers.base import BaseController
from app.exceptions import RecordNotFoundHTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, User as UserSchema
from app.services.user import UserService
from fastapi import HTTPException

class UserController(BaseController[User, UserCreate, UserUpdate, UserSchema]):
    def __init__(self, service: UserService):
        super().__init__(service)
        self.service = service

    async def authenticate(self, email: str, password: str) -> UserSchema:
        try:
            result = await self.service.authenticate(email, password)
            if not result:
                raise HTTPException(status_code=401, detail="Incorrect email or password")
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_by_email(self, email: str) -> UserSchema:
        try:
            return await self.service.get_by_email(email)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
