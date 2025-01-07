from typing import Optional
from pydantic import BaseModel, ConfigDict


class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None
    exercise_type: str

class VideoCreate(VideoBase):
    user_id: int
    file_path: str

class VideoUpdate(VideoBase):
    pass

class VideoInDBBase(VideoBase):
    id: int
    user_id: int
    file_path: str
    model_config = ConfigDict(from_attributes=True)

class Video(VideoInDBBase):
    pass
