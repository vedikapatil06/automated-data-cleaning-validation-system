import pandas as pd

from module1_profiling.profiler import (
    profile_dataset,
    detect_semantic_type,
    detect_suspicious_values,
    analyze_date_formats,
)


def test_semantic_type_detection():
    series = pd.Series([20, 25, 30])

    assert detect_semantic_type("age", series) == "age"


def test_missing_values_are_detected(tmp_path):
    data = pd.DataFrame({
        "customer_id": ["C001", "C002"],
        "age": [25, None],
    })

    file_path = tmp_path / "test_data.csv"
    data.to_csv(file_path, index=False)

    report = profile_dataset(file_path)

    assert report["total_rows"] == 2
    assert report["total_missing_values"] == 1
    assert report["columns"]["age"]["missing_values"] == 1


def test_duplicate_rows_are_detected(tmp_path):
    data = pd.DataFrame({
        "customer_id": ["C001", "C001"],
        "age": [25, 25],
    })

    file_path = tmp_path / "duplicates.csv"
    data.to_csv(file_path, index=False)

    report = profile_dataset(file_path)

    assert report["duplicate_rows"] == 1


def test_invalid_email_is_detected():
    emails = pd.Series(["valid@example.com", "invalid-email"])

    issues = detect_suspicious_values("email", emails)

    assert len(issues) == 1
    assert issues[0]["value"] == "invalid-email"


def test_suspicious_age_is_detected():
    ages = pd.Series([25, 200])

    issues = detect_suspicious_values("age", ages)

    assert len(issues) == 1
    assert issues[0]["value"] == "200"


def test_multiple_date_formats_are_detected():
    dates = pd.Series(["2026-01-10", "2026/01/11"])

    result = analyze_date_formats(dates)

    assert result["has_multiple_formats"] is True
    assert result["format_counts"]["YYYY-MM-DD"] == 1
    assert result["format_counts"]["YYYY/MM/DD"] == 1