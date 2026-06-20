import os

from dotenv import load_dotenv
from google import genai


load_dotenv()
load_dotenv("modules/.env")

GEMINI_MODEL = "gemini-2.5-flash"


class GeminiConfigError(RuntimeError):
    pass


def get_ai_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise GeminiConfigError(
            "Missing GEMINI_API_KEY. Add GEMINI_API_KEY=your_key_here to your .env file."
        )

    return genai.Client(api_key=api_key)
