from fastapi import FastAPI, File, UploadFile, Query
import shutil
import os
from video_processing import process_video

app = FastAPI()

UPLOAD_DIR = "uploads"
PROCESSED_SIR = "processed_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Create uploads folder if it doesn't exist


@app.get("/")
def home():
    return {"message": "FastAPI Backend is running"}


@app.post("/process/")
async def upload_and_process_videos(
    file: UploadFile = File(...),
    dot_size: int = Query(5, description="Size of the dots"),
    dot_spacing: int = Query(5, description="Spacing between dots"),
    brightness_threshold: int = Query(90, description="Brightness of dots"),
):
    """Endpoint to upload a video file."""

    file_location = os.path.join(UPLOAD_DIR, file.filename)

    # Save the file
    # with open(file_location, "wb") as buffer:
    #     buffer.write(await file.read())

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    processed_video_path = process_video(
        file_location,
        f"processed_{file.filename}",
        dot_size,
        dot_spacing,
        brightness_threshold,
    )

    return {"message": "Processing complete!", "processed_video": processed_video_path}
