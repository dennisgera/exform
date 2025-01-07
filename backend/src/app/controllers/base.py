from typing import Any, Generic, List, TypeVar

from app.exceptions import RecordNotFoundHTTPException
from app.services.base import BaseService
from fastapi import HTTPException
from pydantic import BaseModel


ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReturnSchemaType = TypeVar("ReturnSchemaType", bound=BaseModel)

class BaseController(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReturnSchemaType]):
    def __init__(self, service: BaseService[ModelType, CreateSchemaType, UpdateSchemaType, ReturnSchemaType]):
        self.service = service

    async def get_by_id(self, id: Any) -> ReturnSchemaType:
        try:
            result = await self.service.get_by_id(id)
            if not result:
                raise RecordNotFoundHTTPException()
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_all(self) -> List[ReturnSchemaType]:
        try:
            return await self.service.get_all()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create(self, obj_in: CreateSchemaType) -> ReturnSchemaType:
        try:
            return await self.service.create(obj_in)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def update(self, obj_in: UpdateSchemaType, id: Any) -> ReturnSchemaType:
        try:
            result = await self.service.update(obj_in, id)
            if not result:
                raise RecordNotFoundHTTPException()
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def delete(self, id: Any) -> bool:
        try:
            result = await self.service.delete(id)
            if not result:
                raise RecordNotFoundHTTPException()
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))