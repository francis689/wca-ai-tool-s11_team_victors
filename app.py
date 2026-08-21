import json

from src.stage1_analysis import analyze_user_request
from src.stage2_plan import generate_actionable_response
from src.utils import prepare_stage2_analysis, save_history


def main():
    print("======================================")
    print("      RUPSA SACCO AI ASSISTANT")
    print("======================================")

    question = input("\nAsk your RUPSA question: ")

    if not question.strip():
        print("Please enter a question.")
        return

    try:
        print("\n🔎 Analyzing your question...")

        # Stage 1
        stage1_result = analyze_user_request(question)

        print("✅ Stage 1 completed.")

        # Prepare information for Stage 2
        stage1_data = json.loads(stage1_result)
        stage2_analysis = prepare_stage2_analysis(stage1_data)

        print("🧠 Generating RUPSA response...")

        # Stage 2
        final_response = generate_actionable_response(
            question,
            stage2_analysis
        )

        if final_response:
            print("\n======================================")
            print("       RUPSA SACCO RESPONSE")
            print("======================================")
            print(final_response)

            # Save the conversation
            save_history(question, final_response)

            print("\n💾 Conversation saved successfully.")

        else:
            print("\nUnable to generate a response.")

    except Exception as error:
        print(f"\n❌ Error: {error}")


if __name__ == "__main__":
    main()