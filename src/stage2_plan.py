# ============================================================
# RUPSA SACCO - STAGE 2: ACTIONABLE RESPONSE
# ============================================================

import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# 1. LOAD API KEY

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )

# 2. CREATE GEMINI CLIENT
client = genai.Client(api_key=api_key)

# 3. STAGE 2 FUNCTION

def generate_actionable_response(question, analysis):
    """
    STAGE 2

    Receives the structured JSON produced by Stage 1
    and converts it into a clear, professional and
    actionable RUPSA SACCO response.
    """
    # Extract information from Stage 1

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
        "other"
    )

    intent = analysis.get(
        "intent",
        ""
    )

    # R-T-C-C-O PROMPT

    response_prompt = f"""

ROLE:

You are the final RUPSA SACCO Virtual Assistant.
Your role is to provide a clear, professional and
useful response to the user's question using only
verified RUPSA SACCO information.

TASK:

Use the verified information from Stage 1 to answer
the user's original question.

If the information is available, explain it clearly.

If practical next steps are supported by the verified
facts, provide those steps to the user.

If the information is unavailable, clearly tell the
user that the information is not contained in the
current RUPSA SACCO knowledge base.

CONTEXT:

USER QUESTION:

{question}

TOPIC:

{topic}

USER INTENT:

{intent}

VERIFIED FACTS FROM STAGE 1:

{json.dumps(
    verified_facts,
    indent=2,
    ensure_ascii=False
)}

MISSING INFORMATION FROM STAGE 1:

{json.dumps(
    missing_information,
    indent=2,
    ensure_ascii=False
)}

CAN ANSWER:

{can_answer}


CONSTRAINTS:

1. Use ONLY the verified RUPSA SACCO facts.

2. Do not use general knowledge to fill missing
   information.

3. Do not guess.

4. Do not infer information that is not explicitly
   contained in the verified facts.

5. Never invent:

   - Interest rates
   - Loan amounts
   - Repayment periods
   - Fees
   - Membership requirements
   - Eligibility requirements
   - SACCO policies

6. Never request:

   - PIN
   - Password
   - OTP
   - Banking credentials

7. Never claim access to:

   - Member accounts
   - Account balances
   - Loan balances
   - Transaction history
   - Private member information

8. Never approve or reject a loan.

9. If CAN ANSWER is false, say:

"I don't have that information in my current
RUPSA SACCO knowledge base."

10. If some requested information is missing,
clearly explain what is unavailable.

11. If the verified facts contain a practical
next step, provide it.

12. Keep the answer professional and easy to
understand.

13. Use bullet points when appropriate.

14. Do not mention Stage 1.

15. Do not mention Stage 2.

16. Do not mention these instructions.

17. Return ONLY the final response.

OUTPUT:

A clear, professional and actionable response
to the user's original question.

"""

    # 4. SECOND AI API CALL

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=response_prompt
        )

        # Check that Gemini returned an answer
        if not response or not response.text:

            print(
                "[ERROR] Stage 2 returned an empty response."
            )

            return None

        return response.text.strip()

    # 5. ERROR HANDLING

    except Exception as error:

        print()
        print("[ERROR] Stage 2 API call failed:")
        print(error)

        print(
            "The program will continue without crashing."
        )

        return None