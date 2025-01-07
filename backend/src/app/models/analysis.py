from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class Analysis(Base):
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("video.id"), nullable=False)
    pose_data = Column(JSON, nullable=True)  # Store MediaPipe pose landmarks
    feedback = Column(String, nullable=True)  # Store Claude API feedback
    issues_detected = Column(JSON, nullable=True)  # Store specific form issues

    # Relationships
    video = relationship("Video", back_populates="analyses")