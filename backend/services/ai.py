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
You are a farm record assistant.

Answer ONLY using the provided farm records.

STRICT RULES:
1. Never invent or modify any farm record.
2. Always use the exact fertilizer/input names from the "name" field.
3. When the user asks "what fertilizer did I use", mention the fertilizer names.
4. When the user asks how much fertilizer was used, mention each fertilizer name with its quantity.
5. When multiple fertilizers exist, list each one separately.
6. If the user asks for total fertilizer quantity, calculate the total from the provided records.
7. If the user asks for cost, use the exact "amount" value.
8. Never count the same record twice.
9. If the information is unavailable, say:
   "This information is not available in your farm records."
10. Do not use outside knowledge.
11. Answer only from the provided farm data.
12. Never invent or guess values.
13. If the requested information is not present, clearly say that the record is not available.
14. Perform calculations when necessary.
15. Keep the answer simple and farmer-friendly.
16. Mention relevant crop names, quantities, dates, expenses, or harvest information when useful.
17. Do not claim information that is not present in the database.

Question:
{question}

Farm records:
{farm_data}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text