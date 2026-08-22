import json
import streamlit as st
from src.stage1_analysis import analyze_user_request
from src.stage2_plan import generate_actionable_response
from src.utils import prepare_stage2_analysis, save_history

# Set up clean web page configurations
st.set_page_config(page_title="RUPSA SACCO AI Assistant", page_icon="🇰🇪", layout="centered")

def main():
    # Visual Page Headers
    st.title("🇰🇪 RUPSA SACCO AI Assistant")
    st.markdown("---")
    st.write("Welcome! Enter your question below to receive an actionable, policy-compliant response.")

    # 1. Capture User Input via Streamlit Web Text Component box
    question = st.text_input("Ask your RUPSA question:", placeholder="e.g., What are the terms for a School Fees Loan?")

    if question:
        if not question.strip():
            st.warning("Please enter a valid question.")
            return

        # Visual status spinner loops to organize sequential stage tracking UI
        with st.spinner("🔎 Step 1: Processing query parameters (Stage 1)..."):
            try:
                # Execute Stage 1 Call
                stage1_result = analyze_user_request(question)
                
                # Parse JSON results securely
                stage1_data = json.loads(stage1_result)
                stage2_analysis = prepare_stage2_analysis(stage1_data)
                
            except Exception as e:
                st.error(f"❌ Stage 1 Pipeline Failure: {e}")
                return

        with st.spinner("🧠 Step 2: Extracting knowledge base facts & generating roadmap (Stage 2)..."):
            try:
                # Execute Stage 2 Call
                final_response = generate_actionable_response(question, stage2_analysis)
                
            except Exception as e:
                st.error(f"❌ Stage 2 Pipeline Failure: {e}")
                return

        # 2. Display Final Results on the Web Layout View
        if final_response:
            st.success("🎉 Response Generated Successfully!")
            st.markdown("### 📋 RUPSA SACCO RESPONSE")
            
            # Renders markdown response structures cleanly with visual spacing hooks
            st.markdown(final_response)
            
            # Save historical interaction data trail trace logs locally
            save_history(question, final_response)
            st.info("💾 This interaction footprint trace has been logged safely inside outputs/.")
        else:
            st.error("Unable to generate a valid response.")

if __name__ == "__main__":
    main()
