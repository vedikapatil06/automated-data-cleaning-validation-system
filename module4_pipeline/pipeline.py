from pathlib import Path
import json

from module1_profiling.profiler import profile_dataset
from module2_cleaning.cleaner import clean_dataset
from module3_validation.validator import (
    validate_dataset_file,
    run_and_save_advanced_validation,
    print_advanced_validation_summary
)


def run_pipeline(
    input_path="Data/raw_dataset.csv",
    cleaned_path="results/cleaned_data.csv"
):
    """Execute the complete data processing pipeline."""

    print("\n===================================")
    print(" AUTOMATED DATA PROCESSING PIPELINE")
    print("===================================")

    input_file = Path(input_path)
    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Data Profiling
    print("\nSTEP 1: DATA PROFILING")
    print("----------------------")

    profiling_report = profile_dataset(input_file)

    profiling_path = results_dir / "profiling_report.json"

    with open(profiling_path, "w", encoding="utf-8") as file:
        json.dump(profiling_report, file, indent=4, default=str)

    print(f"Profiling report saved: {profiling_path}")

    # Step 2: Data Cleaning
    print("\nSTEP 2: DATA CLEANING")
    print("---------------------")

    cleaned_df, cleaning_log = clean_dataset(
        input_path=input_file,
        output_path=cleaned_path
    )

    print(f"Cleaning completed. Rows remaining: {len(cleaned_df)}")

    # Step 3: Basic Data Validation
    print("\nSTEP 3: BASIC DATA VALIDATION")
    print("-----------------------------")

    validation_report = validate_dataset_file(
        input_path=cleaned_path,
        output_path=results_dir / "validation_report.json"
    )

    print(
        f"Basic validation quality score: "
        f"{validation_report['data_quality_score']}%"
    )

    # Step 4: Advanced Data Validation
    print("\nSTEP 4: ADVANCED DATA VALIDATION")
    print("--------------------------------")

    advanced_result = run_and_save_advanced_validation(
        input_path=cleaned_path
    )

    print_advanced_validation_summary(advanced_result)

    # Final Pipeline Summary
    summary = {
        "pipeline_status": "COMPLETED",
        "input_dataset": str(input_file),
        "cleaned_dataset": str(cleaned_path),
        "profiling_report": str(profiling_path),
        "cleaning_log_entries": len(cleaning_log),
        "basic_validation_score": validation_report[
            "data_quality_score"
        ],
        "advanced_validation_status": advanced_result[
            "report"
        ]["overall_status"]
    }

    summary_path = results_dir / "pipeline_summary.json"

    with open(summary_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, default=str)

    print("\n===================================")
    print(" PIPELINE EXECUTION COMPLETED")
    print("===================================")
    print(f"Pipeline Status: {summary['pipeline_status']}")
    print(f"Summary saved: {summary_path}")

    return summary


if __name__ == "__main__":
    run_pipeline()