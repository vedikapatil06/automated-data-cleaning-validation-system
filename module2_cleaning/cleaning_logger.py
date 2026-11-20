import json
from pathlib import Path
from datetime import datetime


def save_cleaning_log(cleaning_log, output_path="results/cleaning_log.json"):
    """Save cleaning operations into a JSON report."""

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_operations": len(cleaning_log),
        "cleaning_operations": cleaning_log
    }

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, default=str)

    print(f"Cleaning log saved to: {output_file.resolve()}")

    return report