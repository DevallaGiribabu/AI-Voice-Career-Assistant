from fastapi import FastAPI, File, HTTPException, UploadFile

from services.stt import GnaniSTTError, transcribe_audio


MAX_AUDIO_BYTES = 4 * 1024 * 1024

app = FastAPI()


@app.post("/api/transcribe")
async def transcribe(audio: UploadFile = File(...)) -> dict[str, str]:
    audio_data = await audio.read(MAX_AUDIO_BYTES + 1)
    if len(audio_data) > MAX_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="Audio must be 4 MiB or smaller.")

    try:
        transcript = transcribe_audio(
            audio_data=audio_data,
            filename=audio.filename or "audio",
            content_type=audio.content_type or "application/octet-stream",
        )
    except GnaniSTTError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

    return {"transcript": transcript}
