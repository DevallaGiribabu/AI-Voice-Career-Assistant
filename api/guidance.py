from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.career_ai import CareerAIError, generate_career_guidance


class GuidanceRequest(BaseModel):
    transcript: str = Field(min_length=1, max_length=5000)


app = FastAPI()


@app.post("/")
def guidance(request: GuidanceRequest) -> dict[str, str]:
    try:
        answer = generate_career_guidance(request.transcript)
    except CareerAIError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

    return {"guidance": answer}
