import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Load environment variables from the project's .env file
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


# Gemini model
GEMINI_MODEL = "gemini-3.5-flash-lite"

class CareerAIError(Exception):
    """An error that can be safely displayed to the user."""
    pass


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

        # Generate AI response
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        # Get the answer
        answer = response.text

        if not answer or not answer.strip():
            raise CareerAIError(
                "Gemini did not return a valid answer."
            )

        return answer.strip()

    except CareerAIError:
        raise

    except Exception as error:
        # Show the actual detailed error
        raise CareerAIError(
            f"Gemini API error: {type(error).__name__}: {error}"
        ) from None