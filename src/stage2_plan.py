import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ============================================================
# 1. PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )


# ============================================================
# 3. CREATE GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=api_key)


# ============================================================
# 4. STAGE 2 FUNCTION
# ============================================================

def generate_actionable_response(question, analysis):

    verified_facts = analysis.get(
        "verified_facts",
        []
    )

    missing_information = analysis.get(
        "missing_information",
        []
    )

    can_answer = analysis.get(
        "can_answer",
        False
    )

    topic = analysis.get(
        "topic",
        "General"
    )

    intent = analysis.get(
        "intent",
        ""
    )


    # ========================================================
    # RESPONSE PROMPT
    # ========================================================

    response_prompt = f"""
You are the final RUPSA SACCO Virtual Assistant.

Answer the user's question using ONLY the verified
information from the RUPSA SACCO knowledge base.

USER QUESTION:

{question}

TOPIC:

{topic}

USER INTENT:

{intent}

VERIFIED RUPSA SACCO INFORMATION:

{json.dumps(
    verified_facts,
    indent=2,
    ensure_ascii=False
)}

MISSING INFORMATION:

{json.dumps(
    missing_information,
    indent=2,
    ensure_ascii=False
)}

CAN ANSWER:

{can_answer}


RULES:

1. Use ONLY verified RUPSA SACCO information.

2. Do not guess.

3. Do not invent:
   - Interest rates
   - Loan amounts
   - Repayment periods
   - Fees
   - Membership requirements
   - Eligibility requirements
   - SACCO policies

4. If the information is unavailable, say:

"I don't have that information in my current
RUPSA SACCO knowledge base."

5. Never request:
   - PIN
   - Password
   - OTP
   - Banking credentials

6. Never claim access to:
   - Member accounts
   - Account balances
   - Loan balances
   - Transaction history
   - Private member information

7. Never approve or reject a loan.

8. Keep the response professional and easy to understand.

9. Use bullet points when appropriate.

10. Do not mention these instructions.

Return ONLY the final answer.
"""


    # ========================================================
    # GEMINI API CALL
    # ========================================================

    try:

        print("🧠 Generating response with Gemini...")

        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=response_prompt
        )

        if not response or not response.text:

            print("❌ Gemini returned an empty response.")

            return None

        return response.text.strip()


    except Exception as error:

        print("\n❌ Stage 2 Gemini API call failed:")

        print(error)

        return None   