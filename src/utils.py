import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"

HISTORY_FILE = BASE_DIR / "outputs" / "rupsa_sacco_history.txt"


def load_knowledge(topic):
    """
    Load the RUPSA knowledge file that matches the topic.
    """

    topic_files = {
        "Loans": "loans.txt",
        "Membership": "membership.txt",
        "Savings": "savings.txt",
        "General": "about.txt",
    }

    filename = topic_files.get(topic, "about.txt")
    file_path = KNOWLEDGE_DIR / filename

    if not file_path.exists():
        return ""

    return file_path.read_text(encoding="utf-8")


def prepare_stage2_analysis(stage1_output):
    """
    Convert Stage 1 output into the structure expected by Stage 2
    and provide the relevant RUPSA knowledge-base information.
    """

    if isinstance(stage1_output, str):
        stage1_output = json.loads(stage1_output)

    topic = stage1_output.get(
        "inquiry_category",
        "General"
    )

    knowledge = load_knowledge(topic)

    return {
        "verified_facts": [
            knowledge
        ],
        "missing_information": [],
        "can_answer": bool(knowledge.strip()),
        "topic": topic,
        "intent": stage1_output.get(
            "key_variables_extracted",
            ""
        )
    }


def save_history(question, answer):
    """
    Automatically save each RUPSA question and answer.
    """

    HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        HISTORY_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write("\n")
        file.write("=" * 60 + "\n")
        file.write(f"DATE: {timestamp}\n")
        file.write(f"QUESTION: {question}\n")
        file.write(f"ANSWER: {answer}\n")
        file.write("=" * 60 + "\n")