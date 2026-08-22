import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


# ============================================================
# 1. PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


# ============================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(os.path.join(BASE_DIR, ".env"))

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file."
    )


# ============================================================
# 3. CREATE GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=api_key)


# ============================================================
# 4. OUTPUT SCHEMA
# ============================================================

class SaccoAnalysisSchema(BaseModel):

    inquiry_category: str
    target_amount: int
    membership_status: str
    detected_urgency: str
    key_variables_extracted: str


# ============================================================
# 5. STAGE 1 PROMPT
# ============================================================

STAGE_1_PROMPT = """
You are an expert RUPSA SACCO information assistant.

Analyze the user's question and return ONLY valid JSON.

Use exactly this structure:

{
    "inquiry_category": "Loans" or "Membership" or "Savings" or "General",
    "target_amount": 0,
    "membership_status": "Active" or "Inactive" or "Prospect" or "Unknown",
    "detected_urgency": "High" or "Medium" or "Low",
    "key_variables_extracted": "Short description of what the user asked"
}

Rules:

1. Identify the user's main topic.

2. If a loan amount is mentioned, extract it.

3. If membership status is not mentioned,
   use "Unknown".

4. If urgency is not mentioned,
   use "Low".

5. Do not invent information.

6. Return ONLY JSON.
"""


# ============================================================
# 6. ANALYZE USER QUESTION
# ============================================================

def analyze_user_request(user_input: str) -> str:

    print("🚀 Running Gemini...")

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=STAGE_1_PROMPT,
            response_mime_type="application/json",
            response_schema=SaccoAnalysisSchema,
        ),
    )

    return response.text


# ============================================================
# 7. TEST STAGE 1
# ============================================================

if __name__ == "__main__":

    print("======================================")
    print("       RUPSA STAGE 1 - GEMINI")
    print("======================================")

    question = input("\nAsk a RUPSA question: ")

    if not question.strip():
        print("Please enter a question.")
        exit()

    try:

        result = analyze_user_request(question)

        print("\n======================================")
        print("GEMINI STAGE 1 RESULT")
        print("======================================")

        print(result)

        # Check that Gemini returned valid JSON
        json.loads(result)

        print("\n✅ Gemini Stage 1 test successful.")

    except Exception as error:

        print("\n❌ Gemini Stage 1 test failed.")
        print(error)