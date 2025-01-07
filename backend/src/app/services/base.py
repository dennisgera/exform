from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel

from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReturnSchemaType = TypeVar("ReturnSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReturnSchemaType]):
    def __init__(self, repository: BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType], return_schema: type[ReturnSchemaType]):
        self.repository = repository
        self.return_schema = return_schema

    async def get_by_id(self, id: Any) -> Optional[ReturnSchemaType]:
        model = await self.repository.get_by_id(id)
        if model:
            return self.return_schema.model_validate(model)
        return None
    
    async def get_all(self) -> List[ReturnSchemaType]:
        models = await self.repository.get_all()
        return [self.return_schema.model_validate(model) for model in models]
    
    async def create(self, obj_in: CreateSchemaType) -> ReturnSchemaType:
        model = await self.repository.create(obj_in)
        return self.return_schema.model_validate(model)
    
    async def update(self, obj_in: UpdateSchemaType, id: Any) -> Optional[ReturnSchemaType]:
        model = await self.repository.update(obj_in, id)
        if model:
            return self.return_schema.model_validate(model)
        return None
    
    async def delete(self, id: Any) -> bool:
        return await self.repository.delete(id)
        