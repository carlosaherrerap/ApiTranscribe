# Audio Transcription API

This project provides a **FastAPI** backend that uses **OpenAI Whisper** to transcribe uploaded audio files and returns per‑word confidence scores. A lightweight web UI lets you upload an audio file and displays the transcription, highlighting low‑confidence words in red.

## Project Structure
```
apiTranscription/
│   speeching_v2.py   # original script (kept for reference)
│   requirements.txt
│
├─ api/
│   ├─ __init__.py   # (optional, can be empty)
│   ├─ main.py       # FastAPI app with /transcribe endpoint
│   └─ transcribe.py # Whisper wrapper returning confidence scores
│
└─ frontend/
    ├─ index.html    # Simple UI for uploading audio
    └─ style.css     # Modern dark‑mode styling with glassmorphism
```

## Setup
1. **Python 3.9+** is required.
2. Open a terminal in the `apiTranscription` directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note*: Whisper pulls in `torch`. On Windows, the appropriate binary will be installed automatically.

## Running the API
```bash
uvicorn api.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

## Using the Frontend
1. Open `frontend/index.html` in a web browser (you can just double‑click the file).
2. Select an audio file (MP3, WAV, etc.) and click **Transcribir**.
3. The transcription will appear below the button. Words with confidence below `0.8` are highlighted in red.

## Customisation
- **Model size**: Edit `api/transcribe.py` and change `whisper.load_model("base")` to `"small"`, `"tiny"`, etc., for faster or more accurate results.
- **Confidence threshold**: Adjust `confidenceThreshold` in `frontend/index.html`.
- **Styling**: Modify `frontend/style.css` to change colours, fonts, or layout.

---
*Enjoy transcribing!*
