import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

from llm.gemini_utils import generate_content_with_retry


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# =========================================================
# GET API KEY
# =========================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. Check your .env file."
    )

genai.configure(api_key=api_key)


# =========================================================
# TEST REQUEST
# =========================================================

print("Testing Gemini API connection...")

model = genai.GenerativeModel("gemini-2.5-flash")

response = generate_content_with_retry(
    model,
    "You are testing an AI defect analysis system. "
    "Reply with exactly: Gemini connection successful."
)


# =========================================================
# DISPLAY RESULT
# =========================================================

print("\nGemini Response:")
print(response.text)

print("\nGemini API connection test completed successfully.")