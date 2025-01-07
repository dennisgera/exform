import os
from pathlib import Path
import shutil
from uuid import uuid4

from fastapi import UploadFile


UPLOAD_DIR = Path("uploads/videos")

async def save_upload_file(upload_file: UploadFile, user_id: int) -> str:
    """Save an uploaded file to the server and return the file path."""
    # create the directory if it doesn't exist
    user_upload_dir = UPLOAD_DIR / str(user_id)
    user_upload_dir.mkdir(parents=True, exist_ok=True)

    # generate unique filename
    file_extension = Path(upload_file.filename).suffix
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = user_upload_dir / unique_filename

    # save the file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return str(file_path)

async def remove_file(file_path: str) -> bool:
    """Remove a file from the server."""
    try:
        os.remove(file_path)
        return True
    except (FileNotFoundError, OSError):
        return False