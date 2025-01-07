from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base

class ExerciseType(str, enum.Enum):
    SQUAT = "squat"
    DEADLIFT = "deadlift"
    BENCH_PRESS = "bench_press"
    OVERHEAD_PRESS = "overhead_press"
    # Add more exercise types as needed

class Video(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    exercise_type = Column(Enum(ExerciseType), nullable=False)

    # Relationships
    user = relationship("User", back_populates="videos")
    analyses = relationship("Analysis", back_populates="video", cascade="all, delete-orphan")