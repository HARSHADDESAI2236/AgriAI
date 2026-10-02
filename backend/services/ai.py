import os

from dotenv import load_dotenv
from google import genai


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured")


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# AI ANSWER
# =========================================================

async def generate_ai_answer(
    question: str,
    farm_data: str
):

    question_lower = question.lower()

    # =====================================================
    # DIRECT FERTILIZER NAME RESPONSE
    # =====================================================

    if (
        "what fertilizer" in question_lower
        or "which fertilizer" in question_lower
        or "fertilizers did i use" in question_lower
        or "fertilisers did i use" in question_lower
    ):

        # ---------------------------------------------
        # Extract fertilizer names from evidence
        # ---------------------------------------------

        fertilizer_names = []

        records = farm_data

        # The evidence is passed as Python list string.
        # Extract values from "name":
        import re

        names = re.findall(
            r"'name':\s*'([^']+)'",
            records
        )

        for name in names:

            if name not in fertilizer_names:
                fertilizer_names.append(name)

        # ---------------------------------------------
        # No fertilizer records
        # ---------------------------------------------

        if not fertilizer_names:
            return (
                "This information is not available "
                "in your farm records."
            )

        # ---------------------------------------------
        # Build natural answer
        # ---------------------------------------------

        if len(fertilizer_names) == 1:

            return (
                f"You used {fertilizer_names[0]}."
            )

        if len(fertilizer_names) == 2:

            return (
                f"You used {fertilizer_names[0]} "
                f"and {fertilizer_names[1]}."
            )

        return (
            "You used "
            + ", ".join(fertilizer_names[:-1])
            + f", and {fertilizer_names[-1]}."
        )

    # =====================================================
    # GEMINI FOR OTHER QUESTIONS
    # =====================================================

    prompt = f"""
You are a farm record assistant.

Answer ONLY using the provided farm records.

STRICT RULES:

1. Never invent or modify any farm record.

2. Always use exact values from the records.

3. Never count the same record twice.

4. If the user asks how much fertilizer was used,
   mention each fertilizer name and its quantity.

5. If the user asks for total fertilizer quantity,
   calculate the total from the provided records.

6. If the user asks for cost,
   use the exact "amount" values from the records.

7. Do not use outside knowledge.

8. Never invent or guess values.

9. If the requested information is not present, say:

"This information is not available in your farm records."

10. Keep the answer simple and farmer-friendly.

11. Mention the crop name when it is available.

12. Use exact fertilizer/input names from the records.

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