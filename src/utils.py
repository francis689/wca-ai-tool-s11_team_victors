import json
import os


def prepare_stage2_analysis(stage1_data):
    """
    Prepare Stage 1 analysis for Stage 2 processing.
    """
    if not isinstance(stage1_data, dict):
        raise ValueError("Stage 1 data must be a dictionary.")

    return {
        "inquiry_category": stage1_data.get("inquiry_category", "Unknown"),
        "target_amount": stage1_data.get("target_amount", 0),
        "membership_status": stage1_data.get("membership_status", "Unknown"),
        "detected_urgency": stage1_data.get("detected_urgency", "Unknown"),
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
        json.dump(data, file, indent=4, ensure_ascii=False)

    return filepath


def export_text(data, filename="output.txt"):
    """Export data to a text file."""
    os.makedirs("outputs", exist_ok=True)

    filepath = os.path.join("outputs", filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(str(data))

    return filepath

if __name__ == "__main__":
    test_data = {
        "inquiry_category": "Loans",
        "target_amount": 300000,
        "membership_status": "Active",
        "detected_urgency": "High",
        "key_variables_extracted": "Development loan"
    }
    print(prepare_stage2_analysis(test_data))

