
import os
from pathlib import Path

from dotenv import load_dotenv
from crewai import LLM

# Load environment variables
PROJECT_ROOT = Path(__file__).resolve().parent

load_dotenv(PROJECT_ROOT / ".env", override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL")


def test_gemini():

    if not API_KEY:
        raise ValueError("GEMINI_API_KEY is missing!")

    if not MODEL:
        raise ValueError("GEMINI_MODEL is missing!")

    print("Connecting to Gemini API...")

    llm = LLM(
        model=MODEL,
        api_key=API_KEY,
        temperature=0.3,
    )

    response = llm.call(
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: Leo AI Tutor is ready."
            }
        ]
    )

    print("\nGemini Response:")
    print(response)

    print("\nGemini API Connected Successfully!")


if __name__ == "__main__":
    test_gemini()
