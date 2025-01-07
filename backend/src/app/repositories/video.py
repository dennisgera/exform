from app.models.video import Video
from app.repositories.base import BaseRepository
from app.schemas.video import VideoCreate, VideoUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class VideoRepository(BaseRepository[Video, VideoCreate, VideoUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(Video, db)

    async def get_user_videos(self, user_id: int) -> list[Video]:
        query = select(self.model).where(self.model.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()