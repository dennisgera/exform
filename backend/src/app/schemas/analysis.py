from typing import Optional

from pydantic import BaseModel, ConfigDict


class AnalysisBase(BaseModel):
    feedback: Optional[str] = None
    issues_detected: Optional[dict] = None

class AnalysisCreate(AnalysisBase):
    video_id: int
    pose_data: Optional[dict] = None

class AnalysisUpdate(AnalysisBase):
    pose_data: Optional[dict] = None

class AnalysisInDBBase(AnalysisBase):
    id: int
    video_id: int
    pose_data: Optional[dict] = None
    model_config = ConfigDict(from_attributes=True)

class Analysis(AnalysisInDBBase):
    pass
