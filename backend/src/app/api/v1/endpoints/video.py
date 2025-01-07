from app.api.v1.deps import get_current_active_user, get_video_controller
from app.controllers.video import VideoController
from app.schemas.video import Video
from app.schemas.user import User
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile

router = APIRouter()


@router.post("/upload", response_model=Video)
async def upload_video(
    title: str = Form(...),
    exercise_type: str = Form(...),
    description: str = Form(None),
    file: UploadFile = Form(...),
    current_user: User = Depends(get_current_active_user),
    video_controller: VideoController = Depends(get_video_controller),
):
    """Upload a new video for form analysis."""
    return await video_controller.upload_video(
        user_id=current_user.id,
        title=title,
        exercise_type=exercise_type,
        file=file,
        description=description,
    )


@router.get("/my-videos", response_model=list[Video])
async def get_user_videos(
    current_user: User = Depends(get_current_active_user),
    video_controller: VideoController = Depends(get_video_controller),
):
    """Get all videos uploaded by the current user."""
    return await video_controller.get_user_videos(current_user.id)


@router.get("/{video_id}", response_model=Video)
async def get_video(
    video_id: int,
    current_user: User = Depends(get_current_active_user),
    video_controller: VideoController = Depends(get_video_controller),
):
    """Get a video by ID."""
    video = await video_controller.get_by_id(video_id)
    if video.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return video


@router.delete("/{video_id}")
async def delete_video(
    video_id: int,
    current_user: User = Depends(get_current_active_user),
    video_controller: VideoController = Depends(get_video_controller),
):
    """Delete a video by ID."""
    video = await video_controller.get_by_id(video_id)
    if video.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await video_controller.delete(video_id)
