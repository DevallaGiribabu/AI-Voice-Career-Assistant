import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

STT_ENDPOINT = "https://api.vachana.ai/stt/v3"
STT_MODEL = "prisma-v3.0"
STT_LANGUAGE_CODE = "indic-auto"
STT_TIMEOUT_SECONDS = 60


class GnaniSTTError(Exception):
    """An error that can be safely displayed to the user."""


def transcribe_audio(
    audio_data: bytes, filename: str, content_type: str
) -> str:
    """Send uploaded audio to Gnani STT and return its transcript."""
    api_key = os.getenv("GNANI_API_KEY")
    if not api_key:
        raise GnaniSTTError("GNANI_API_KEY is not configured in the environment.")
    if not audio_data:
        raise GnaniSTTError("The uploaded audio file is empty.")

    try:
        response = requests.post(
            STT_ENDPOINT,
            headers={"X-API-Key-ID": api_key},
            files={"audio_file": (filename, audio_data, content_type)},
            data={
                "model": STT_MODEL,
                "language_code": STT_LANGUAGE_CODE,
            },
            timeout=STT_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.HTTPError as error:
        status_code = error.response.status_code if error.response is not None else "unknown"
        raise GnaniSTTError(
            f"Gnani STT returned an HTTP error (status {status_code})."
        ) from None
    except requests.RequestException:
        raise GnaniSTTError(
            "Could not connect to Gnani STT. Check your connection and try again."
        ) from None

    try:
        result = response.json()
    except ValueError:
        raise GnaniSTTError("Gnani STT returned a response that was not valid JSON.") from None

    if not isinstance(result, dict) or result.get("success") is not True:
        raise GnaniSTTError("Gnani STT did not report a successful transcription.")

    transcript = result.get("transcript")
    if not isinstance(transcript, str) or not transcript.strip():
        raise GnaniSTTError("Gnani STT response did not contain a valid transcript.")

    return transcript
