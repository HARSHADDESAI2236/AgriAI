import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=GEMINI_API_KEY)


async def generate_ai_answer(question: str, farm_data: str):
    prompt = f"""
You are AgriAI, an AI assistant for farmers.

The farmer asked:
{question}

Below is the farmer's actual farm data retrieved from the database:

{farm_data}

RULES:
1. Answer ONLY using the provided farm data.
2. Never invent or guess values.
3. If the requested information is not present, clearly say that the record is not available.
4. Perform calculations when necessary.
5. Keep the answer simple and farmer-friendly.
6. Mention relevant crop names, quantities, dates, expenses or harvest information when useful.
7. Do not claim information that is not present in the database.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text