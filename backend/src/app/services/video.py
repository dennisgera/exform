from app.models.video import Video
from app.repositories.video import VideoRepository
from app.schemas.video import VideoCreate, VideoUpdate, Video as VideoSchema
from app.services.base import BaseService
from app.utils.file_storage import remove_file, save_upload_file
from fastapi import UploadFile


class VideoService(BaseService[Video, VideoCreate, VideoUpdate, VideoSchema]):
    repository: VideoRepository

    def __init__(self, repository: VideoRepository):
        super().__init__(repository, VideoSchema)
        self.repository = repository

    async def get_user_videos(self, user_id: int) -> list[VideoSchema]:
        videos = await self.repository.get_user_videos(user_id)
        return [self.return_schema.model_validate(video) for video in videos]
    
    async def create_with_file(
            self, 
            user_id: int,
            title: str,
            exercise_type: str,
            file: UploadFile,
            description: str = None
        ) -> VideoSchema:
        # save the uploaded file
        file_path = await save_upload_file(file, user_id)
        
        # create the video record
        video_in = VideoCreate(
            title=title,
            exercise_type=exercise_type,
            description=description,
            file_path=file_path,
            user_id=user_id
        )
        return await self.create(video_in)
    
    async def delete(self, id: int) -> bool:
        # get video before deletion to get the file path
        video = await self.repository.get_by_id(id)
        if video:
            # delete file from storage
            await remove_file(video.file_path)
            
            # delete database record
            return await self.repository.delete(id)
        return False
