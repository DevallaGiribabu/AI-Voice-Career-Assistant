import logging
import os
from pathlib import Path
import time

from dotenv import load_dotenv
from google import genai


# Load environment variables from the project's .env file
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


# Gemini model
GEMINI_MODEL = "gemini-3.5-flash-lite"
GEMINI_FALLBACK_MODEL = "gemini-2.5-flash"
GEMINI_MODELS = (GEMINI_MODEL, GEMINI_FALLBACK_MODEL)
MAX_ATTEMPTS_PER_MODEL = 2
RETRY_DELAY_SECONDS = 1
RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}

logger = logging.getLogger(__name__)

class CareerAIError(Exception):
    """An error that can be safely displayed to the user."""
    pass


def _is_retryable(error: Exception) -> bool:
    status_code = getattr(error, "code", None) or getattr(error, "status_code", None)
    try:
        if int(status_code) in RETRYABLE_STATUS_CODES:
            return True
    except (TypeError, ValueError):
        pass

    status = str(getattr(error, "status", "")).upper()
    message = str(error).upper()
    return status in {"RESOURCE_EXHAUSTED", "UNAVAILABLE", "INTERNAL"} or any(
        f"{code} " in message or f"{code}:" in message
        for code in RETRYABLE_STATUS_CODES
    )


def generate_career_guidance(user_question: str) -> str:
    """Generate practical career guidance for the user's question."""

    # Get Gemini API key
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise CareerAIError(
            "GEMINI_API_KEY is not configured in the environment."
        )

    # Check if the question is empty
    if not user_question or not user_question.strip():
        raise CareerAIError(
            "Please provide a career-related question."
        )

    # Create the prompt
    prompt = f"""
You are an AI Career Guidance Assistant.

Help the user with:
- AI and software careers
- Learning roadmaps
- Projects
- Resume preparation
- Interview preparation
- Skills required for jobs

Give clear, simple, practical, and encouraging advice.

User's question:
{user_question.strip()}
"""

    try:
        # Create Gemini client
        client = genai.Client(api_key=api_key)

        last_error = None
        for model_index, model in enumerate(GEMINI_MODELS):
            for attempt in range(MAX_ATTEMPTS_PER_MODEL):
                try:
                    response = client.models.generate_content(
                        model=model,
                        contents=prompt,
                    )
                    answer = response.text
                    if not answer or not answer.strip():
                        raise CareerAIError(
                            "Gemini did not return a valid answer."
                        )
                    return answer.strip()
                except CareerAIError:
                    raise
                except Exception as error:
                    last_error = error
                    if not _is_retryable(error):
                        raise CareerAIError(
                            f"Gemini API error: {type(error).__name__}: {error}"
                        ) from None

                    if attempt + 1 < MAX_ATTEMPTS_PER_MODEL:
                        logger.warning(
                            "Gemini model %s returned a temporary error; retrying.",
                            model,
                        )
                        time.sleep(RETRY_DELAY_SECONDS)
                    elif model_index + 1 < len(GEMINI_MODELS):
                        logger.warning(
                            "Gemini model %s remains unavailable; switching to fallback.",
                            model,
                        )

        logger.error(
            "All configured Gemini models failed with retryable errors: %s",
            type(last_error).__name__ if last_error else "unknown error",
        )
        raise CareerAIError(
            "Gemini is temporarily busy. Please retry your career guidance in a moment."
        ) from None

    except CareerAIError:
        raise
    except Exception as error:
        raise CareerAIError(
            f"Gemini API error: {type(error).__name__}: {error}"
        ) from None