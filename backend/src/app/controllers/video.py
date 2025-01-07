from fastapi import HTTPException, UploadFile
from app.models.video import Video
from app.schemas.video import VideoCreate, VideoUpdate, Video as VideoSchema
from app.controllers.base import BaseController
from app.services.video import VideoService
from app.db.session import get_db

class VideoController(BaseController[Video, VideoCreate, VideoUpdate, VideoSchema]):
    def __init__(self, service: VideoService):
        super().__init__(service)
        self.service = service

    async def get_user_videos(self, user_id: int) -> list[VideoSchema]:
        try:
            return await self.service.get_user_videos(user_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def upload_video(
            self, 
            user_id: int,
            title: str,
            exercise_type: str,
            file: UploadFile,
            description: str = None
    ) -> VideoSchema:
        # validate file type
        if not file.content_type.startswith("video/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Only video files are allowed.")
        try:
            return await self.service.create_with_file(
                user_id=user_id,
                title=title,
                exercise_type=exercise_type,
                file=file,
                description=description
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    

    