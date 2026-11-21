import json
import pandas as pd

import module4_pipeline.pipeline as pipeline


def test_run_pipeline_successfully(tmp_path, monkeypatch):
    # Create a temporary input dataset
    input_file = tmp_path / "raw_dataset.csv"
    input_file.write_text("customer_id\nC001\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    # Mock profiling
    monkeypatch.setattr(
        pipeline,
        "profile_dataset",
        lambda path: {"total_rows": 1}
    )

    # Mock cleaning
    def mock_clean_dataset(input_path, output_path):
        output_file = tmp_path / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text("customer_id\nC001\n", encoding="utf-8")

        return pd.DataFrame({"customer_id": ["C001"]}), ["Cleaning completed"]

    monkeypatch.setattr(
        pipeline,
        "clean_dataset",
        mock_clean_dataset
    )

    # Mock basic validation
    monkeypatch.setattr(
        pipeline,
        "validate_dataset_file",
        lambda input_path, output_path: {
            "data_quality_score": 87.5
        }
    )

    # Mock advanced validation
    monkeypatch.setattr(
        pipeline,
        "run_and_save_advanced_validation",
        lambda input_path: {
            "report": {"overall_status": "PASSED"},
            "saved_path": "results/advanced_validation_report.json"
        }
    )

    monkeypatch.setattr(
        pipeline,
        "print_advanced_validation_summary",
        lambda result: None
    )

    # Run pipeline
    summary = pipeline.run_pipeline(
        input_path=input_file,
        cleaned_path="results/cleaned_data.csv"
    )

    # Verify results
    assert summary["pipeline_status"] == "COMPLETED"
    assert summary["basic_validation_score"] == 87.5
    assert summary["advanced_validation_status"] == "PASSED"

    summary_file = tmp_path / "results" / "pipeline_summary.json"
    assert summary_file.exists()

    saved_summary = json.loads(summary_file.read_text(encoding="utf-8"))
    assert saved_summary["pipeline_status"] == "COMPLETED"