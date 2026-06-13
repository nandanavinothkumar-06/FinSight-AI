import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def ask_gemini(prompt):

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception:

        return """
⚠️ FinSight Copilot is currently unavailable.

The AI service has reached its usage limit or is temporarily unavailable.

Please try again later.
"""