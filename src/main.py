import os
import json
from dotenv import load_dotenv

# =========================================================
# 1. SETUP ENVIRONMENT CONFIGURATIONS
# =========================================================
load_dotenv()
api_token = os.getenv("OPENAI_API_KEY")

# Force Simulation Mode to True so it runs entirely offline without an API key!
SIMULATION_MODE = True
print("ℹ️ Running in OFFLINE SIMULATION MODE for testing.")

# =========================================================
# 2. LOCAL DATA RETRIEVAL SCANNER (The RAG Core)
# =========================================================
def local_file_retrieval(keywords_list):
    """
    Scans the local RUPSA SACCO handbook text file line by line
    and extracts lines containing any matching search keywords.
    """
    matched_lines = []
    file_path = "data/rupsa_handbook.txt"
    
    if not os.path.exists(file_path):
        print(f"⚠️ Reference source data file missing at: {file_path}")
        return ""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            handbook_lines = file.readlines()
            
        for line in handbook_lines:
            if any(keyword.strip().lower() in line.lower() for keyword in keywords_list if keyword.strip()):
                matched_lines.append(line.strip())
                
    except Exception as e:
        print(f"❌ Failed reading text data file: {str(e)}")
        
    return "\n".join(matched_lines)

# =========================================================
# 3. THE TWO-STAGE CONNECTED RAG PIPELINE
# =========================================================
def run_sacco_assistant():
    print("\n--- NEW MEMBER QUERY INTERFACE ---")
    member_query = input("💬 Ask a question about RUPSA SACCO (e.g., What are the terms for an emergency loan?): ")
    
    if not member_query.strip():
        print("⚠️ Validation Failure: User query input cannot be empty. Please try again.")
        return

    try:
        # --- STAGE 1: KEYWORD EXTRACTION ---
        print("\n⚙️ [Simulating Stage 1 API Call Outcome...]")
        if "loan" in member_query.lower() or "emergency" in member_query.lower():
            raw_json_output = '{"search_keywords": ["emergency loan", "interest", "repayment"]}'
        elif "member" in member_query.lower() or "join" in member_query.lower():
            raw_json_output = '{"search_keywords": ["membership", "contribution", "capital"]}'
        else:
            raw_json_output = '{"search_keywords": ["loan", "requirements"]}'
        
        # Try/Except JSON parsing test block
        parsed_data = json.loads(raw_json_output)
        extracted_keywords = parsed_data.get("search_keywords", [])
        
        print("\n=== STAGE 1 JSON PACKET DISPLAY ===")
        print(json.dumps(parsed_data, indent=4))
        print(f"🔍 Local Scanner searching document index for: {extracted_keywords}")

        # --- RUN RETRIEVAL LOGIC STEP ---
        retrieved_context = local_file_retrieval(extracted_keywords)
        
        if not retrieved_context:
            retrieved_context = "No direct matching handbook guidelines found."

        # --- STAGE 2: ANSWER GENERATION ---
        print("\n⚙️ [Simulating Stage 2 Contextual Synthesis Answer...]")
        final_answer = f"### RUPSA SACCO Agent Response\nBased on your query, here are the matching rules located in our reference document:\n\n{retrieved_context}\n\nFor deeper clarifications, contact info@rupsasacco.com."
        
        print("\n=== STAGE 2 FINAL RESOLUTION ===")
        print(final_answer)

        # --- EXPORT REPORT LOG TO FILE ---
        output_directory = "data/processed"
        os.makedirs(output_directory, exist_ok=True)
        export_file_path = os.path.join(output_directory, "member_resolution.md")
        
        with open(export_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(f"# RUPSA SACCO SYSTEM REPORT\n\n")
            output_file.write(f"## Member Question:\n{member_query}\n\n")
            output_file.write(f"## Context Retrieved:\n{retrieved_context}\n\n")
            output_file.write(f"## Final Answer:\n{final_answer}\n")
            
        print(f"\n💾 Operation successful! Ledger report written to: {export_file_path}")

    except json.JSONDecodeError:
        print("❌ Error: Failed to parse raw data block to valid JSON format.")
    except Exception as e:
        print(f"❌ Network Call Pipeline Disruption: {str(e)}")

# =========================================================
# 4. INTERACTIVE DASHBOARD MENU
# =========================================================
def display_dashboard():
    while True:
        print("\n==========================================")
        print("🏛️  RUPSA SACCO AUTOMATED PORTAL")
        print("==========================================")
        print("1. Query Member Services & Loan Products")
        print("2. Exit System Console")
        print("------------------------------------------")
        user_selection = input("Choose a menu action item (1-2): ").strip()

        if user_selection == "1":
            run_sacco_assistant()
        elif user_selection == "2":
            print("\nShutting down portal console log. Goodbye! 👋")
            break
        else:
            print("❌ Input validation error: Please type '1' or '2'.")

if __name__ == "__main__":
    display_dashboard()