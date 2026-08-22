import json
import os
from pathlib import Path
from datetime import datetime


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
HISTORY_FILE = OUTPUTS_DIR / "rupsa_sacco_history.txt"


def parse_json(data):
    """
    Safely parse Stage 1 JSON data.

    Accepts either:
    - A Python dictionary
    - A JSON string
    """
    if isinstance(data, dict):
        return data

    if not isinstance(data, str):
        raise ValueError(
            "Stage 1 data must be a dictionary or JSON string."
        )

    try:
        return json.loads(data)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON from Stage 1: {error}"
        ) from error


def prepare_stage2_analysis(stage1_data):
    """
    FIXED PIPELINE BRIDGE: 
    Takes Wilfred's Stage 1 JSON schema and translates it into the precise
    format Sarah's Stage 2 code expects, while dynamically injecting 
    verified facts from the local knowledge base directory.
    """
    # 1. Safely parse the raw JSON data string from Stage 1 into a python dict
    parsed_json = parse_json(stage1_data)

    # 2. Extract values mapped by Wilfred's Stage 1 code module
    category = parsed_json.get("inquiry_category", "General").strip()
    intent_summary = parsed_json.get("key_variables_extracted", "")
    
    verified_facts = []
    missing_information = []
    can_answer = False

    # 3. Dynamic Knowledge Mapping using Francis's committed text files
    # Maps categories to files (normalized to lower-case matches)
    file_map = {
        "loans": "knowledge/loans.txt",
        "membership": "knowledge/membership.txt",
        "savings": "knowledge/savings.txt",
        "general": "knowledge/about.txt"
    }

    # Normalize name to lookup file target path location mapping
    target_key = category.lower()
    target_file_path = BASE_DIR / file_map.get(target_key, "knowledge/about.txt")

    # 4. Check if the file exists locally and read its contents directly
    if target_file_path.exists():
        try:
            with open(target_file_path, "r", encoding="utf-8") as file:
                # Read all file text parameters as verified background facts
                content_lines = file.readlines()
                verified_facts = [line.strip() for line in content_lines if line.strip()]
                can_answer = True
        except Exception as file_error:
            missing_information.append(f"Failed reading internal server asset: {file_error}")
    else:
        # Emergency backup fallback block: If category matching drifts, use the loans table
        backup_path = BASE_DIR / "knowledge/loans.txt"
        if backup_path.exists():
            with open(backup_path, "r", encoding="utf-8") as file:
                verified_facts = [line.strip() for line in file.readlines() if line.strip()]
                can_answer = True
        else:
            missing_information.append(f"Target resource document mapping path not found: {target_file_path.name}")

    # 5. Output the exact dictionary schema structure Sarah's Stage 2 file needs
    return {
        "verified_facts": verified_facts,
        "missing_information": missing_information,
        "can_answer": can_answer,
        "topic": category,
        "intent": intent_summary
    }



def handle_error(error):
    """Return a clean error message."""
    return f"Error: {str(error)}"


def export_json(data, filename="output.json"):
    """Export data to a JSON file."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    filepath = OUTPUTS_DIR / filename

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    return str(filepath)


def export_text(data, filename="output.txt"):
    """Export data to a text file."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    filepath = OUTPUTS_DIR / filename

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(str(data))

    return str(filepath)


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