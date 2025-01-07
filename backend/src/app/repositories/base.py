from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql import update
from app.utils.date import now


ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[ModelType]:
        query = select(self.model)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        model = self.model(**obj_in.model_dump())
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def update(self, obj_in: UpdateSchemaType, id: Any) -> Optional[ModelType]:
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .execution_options(synchronize_session="fetch")
            .returning(self.model)
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete(self, id: Any) -> bool:
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(deleted_at=now())
            .execution_options(synchronize_session="fetch")
            .returning(self.model)
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return bool(result.scalar_one_or_none())
