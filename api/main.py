# main.py
"""FastAPI application exposing a /transcribe endpoint.
Accepts an audio file upload, runs Whisper transcription with confidence scores,
and returns JSON response.
"""

import os
import shutil
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .transcribe import transcribe_with_confidence

app = FastAPI(title="Audio Transcription API")

# Root endpoint providing a simple health check
@app.get("/")
async def root():
    return {"message": "Audio Transcription API is running. Use /transcribe to POST audio files."}


# Allow frontend (served from same origin or different) to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for temporary uploads
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    # Save to temporary location
    temp_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)
    try:
        with open(temp_path, "wb") as out_file:
            content = await file.read()
            out_file.write(content)
        # Run transcription
        result = transcribe_with_confidence(temp_path)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
