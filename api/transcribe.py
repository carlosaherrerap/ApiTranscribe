# transcribe.py
"""Utility module for transcribing audio files using OpenAI Whisper.
Provides per‑word confidence scores.
"""

import os
from typing import List, Dict, Any

# On Windows, Whisper's internal libc loading can fail. Setting this env var disables that behavior.
if os.name == "nt":
    os.environ["WHISPER_NO_LIBC"] = "1"

import whisper

# Load model once at import time for efficiency. Using "base" for a balance of speed/accuracy.
# Users can change to "small" or "tiny" if desired.
_model = whisper.load_model("base")

def transcribe_with_confidence(audio_path: str) -> Dict[str, Any]:
    """Transcribe an audio file and return text with per‑word confidence.

    Returns a dictionary with:
        - "text": full transcription string
        - "words": list of dicts {"word": str, "confidence": float}
    """
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Whisper's transcribe returns a result with "segments" and optionally "words" if the model supports it.
    result = _model.transcribe(audio_path, word_timestamps=True)
    # Full text
    text = result.get("text", "").strip()
    # Extract words with confidence if available
    words_info: List[Dict[str, Any]] = []
    # Newer whisper versions provide "words" list directly.
    if "words" in result:
        for w in result["words"]:
            # Each entry contains "word" and "confidence"
            words_info.append({"word": w["word"].strip(), "confidence": float(w.get("confidence", 0.0))})
    else:
        # Fallback: split text into words and assign a dummy confidence of 1.0
        for w in text.split():
            words_info.append({"word": w, "confidence": 1.0})
    return {"text": text, "words": words_info}
