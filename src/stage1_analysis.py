import os
import json

from google import genai
from google.genai import types
from pydantic import BaseModel  # <-- Direct Pydantic import to fix the error

# =====================================================================
# SECTION 1: R-T-C-C-O FRAMEWORK PROMPT DEFINITIONS
# =====================================================================
STAGE_1_PROMPT = """
ROLE: You are an expert financial auditor and data extraction compliance analyst for RUPSA SACCO.

TASK: Analyze the user's raw inquiry text and pull out key structural parameters into an organized data architecture.

CONTEXT: The user is interacting with a SACCO interface regarding dynamic account options, loan applications, financial eligibility parameters, or updates.

CONSTRAINT: You must output ONLY a valid JSON object matching the requested schema layout. Do not include markdown code block syntax (like ```json), backticks, or conversational text. If a variable is missing, set its value to "Unknown".

OUTPUT: Return a valid JSON object matching this schema blueprint layout exactly:
{
    "inquiry_category": "Loans" or "Membership" or "Savings" or "General",
    "target_amount": 0,
    "membership_status": "Active" or "Inactive" or "Prospect" or "Unknown",
    "detected_urgency": "High" or "Medium" or "Low",
    "key_variables_extracted": "A short brief sentence of what they mentioned"
}
"""

# Structural schema definition utilizing pure Pydantic compliance
class SaccoAnalysisSchema(BaseModel):
    inquiry_category: str
    target_amount: int
    membership_status: str
    detected_urgency: str
    key_variables_extracted: str

# =====================================================================
# SECTION 2: HYBRID CALL ROUTER (WITH AUTOMATIC FALLBACK)
# =====================================================================
def analyze_user_request(user_input: str) -> str:
    """
    Attempts to process the inquiry via OpenAI. 
    If a quota/balance limit (429) is hit, it automatically falls back to Gemini.
    """
    
    # --- Try OpenAI Primary Strategy First ---
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and "sk-proj-EMKYQ" not in openai_key and "your_key" not in openai_key:
        try:
            print("🤖 Attempting primary processing via OpenAI (gpt-4o-mini)...")
            openai_client = OpenAI(api_key=openai_key)
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": STAGE_1_PROMPT},
                    {"role": "user", "content": f"User Raw Inquiry: {user_input}"}
                ],
                temperature=0.1
            )
            return response.choices.message.content
            
        except Exception as e:
            print(f"⚠️ OpenAI call dropped or ran out of credits. Error details: {e}")
            print("🔄 Initializing failover protocol...")
            
        # --- Fallback to Google Gemini ---
    print("🚀 Running fallback engine via Google Gemini (gemini-3.6-flash)...")
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("Critical Error: Both OpenAI and Gemini API keys are missing or invalid inside .env file.")
        
    gemini_client = genai.Client(api_key=gemini_key)
    
    response = gemini_client.models.generate_content(
        model='gemini-3.6-flash',  # <-- Fixed model name here
        contents=f"User Raw Inquiry: {user_input}",
        config=types.GenerateContentConfig(
            system_instruction=STAGE_1_PROMPT,
            temperature=0.1,
            response_mime_type="application/json",
            response_schema=SaccoAnalysisSchema,  # Schema enforcement
        ),
    )
    return response.text

# =====================================================================
# SECTION 3: LOCAL TESTING MATRIX
# =====================================================================
if __name__ == "__main__":
    from dotenv import load_dotenv
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(base_dir, ".env")
    load_dotenv(dotenv_path=dotenv_path)
    
    print("🧪 [STAGE 1] Testing Local Dual-Engine Hybrid Module...")
    sample_query = "I have been an active member of RUPSA for 2 years. Can I apply for a development loan of 300,000 Ksh urgently?"
    
    try:
        raw_output = analyze_user_request(sample_query)
        print("\n✅ Final Extracted JSON Output:")
        print(raw_output)
        
        parsed_test = json.loads(raw_output)
        print("\n🎉 Verification Success: System returned clean structural JSON!")
        
    except Exception as e:
        print(f"\n❌ Local Execution Matrix Failed: {e}")
