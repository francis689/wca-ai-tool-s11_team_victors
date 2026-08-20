import json
import os


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
    Prepare Stage 1 analysis for Stage 2 processing.
    Safely parses and validates Stage 1 data.
    """
    stage1_data = parse_json(stage1_data)

    return {
        "inquiry_category": stage1_data.get(
            "inquiry_category",
            "Unknown"
        ),
        "target_amount": stage1_data.get(
            "target_amount",
            0
        ),
        "membership_status": stage1_data.get(
            "membership_status",
            "Unknown"
        ),
        "detected_urgency": stage1_data.get(
            "detected_urgency",
            "Unknown"
        ),
        "key_variables_extracted": stage1_data.get(
            "key_variables_extracted",
            ""
        )
    }


def handle_error(error):
    """Return a clean error message."""
    return f"Error: {str(error)}"


def export_json(data, filename="output.json"):
    """Export data to a JSON file."""
    os.makedirs("outputs", exist_ok=True)

    filepath = os.path.join("outputs", filename)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    return filepath


def export_text(data, filename="output.txt"):
    """Export data to a text file."""
    os.makedirs("outputs", exist_ok=True)

    filepath = os.path.join("outputs", filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(str(data))

    return filepath

