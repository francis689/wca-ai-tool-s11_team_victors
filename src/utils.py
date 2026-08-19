import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


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