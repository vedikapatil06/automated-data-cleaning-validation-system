import pandas as pd
import pytest
import json

from module3_validation.validator import (
    validate_required_columns,
    validate_data_types,
    validate_numeric_ranges,
    validate_email_format,
    validate_date_format,
    validate_missing_values,
    validate_duplicates,
    detect_anomalies,
    run_all_validations,
    save_validation_report,
    validate_dataset_file
)


# 1. Required Column Validation
def test_required_columns():
    df = pd.DataFrame({
        "name": ["Vedika"],
        "age": [21]
    })

    result = validate_required_columns(
        df, ["name", "age"]
    )

    assert result["passed"] is True


def test_missing_required_columns():
    df = pd.DataFrame({"name": ["Vedika"]})

    result = validate_required_columns(
        df, ["name", "age"]
    )

    assert result["passed"] is False
    assert "age" in result["missing_columns"]


# 2. Data Type Validation
def test_data_type_validation():
    df = pd.DataFrame({"age": pd.Series([20, 21], dtype="int64")})

    result = validate_data_types(
        df, {"age": "int64"}
    )

    assert result["passed"] is True


def test_invalid_data_type():
    df = pd.DataFrame({"age": ["20", "21"]})

    result = validate_data_types(
        df, {"age": "int64"}
    )

    assert result["passed"] is False


# 3. Numeric Range Validation
def test_numeric_range_validation():
    df = pd.DataFrame({"age": [20, 25, 30]})

    result = validate_numeric_ranges(
        df, {"age": (1, 100)}
    )

    assert result["passed"] is True


def test_invalid_numeric_range():
    df = pd.DataFrame({"age": [20, 150]})

    result = validate_numeric_ranges(
        df, {"age": (1, 100)}
    )

    assert result["passed"] is False


# 4. Email Validation
def test_valid_email():
    df = pd.DataFrame({
        "email": ["test@gmail.com"]
    })

    result = validate_email_format(df, ["email"])

    assert result["passed"] is True


def test_invalid_email():
    df = pd.DataFrame({
        "email": ["invalid-email"]
    })

    result = validate_email_format(df, ["email"])

    assert result["passed"] is False


# 5. Date Validation
def test_valid_date():
    df = pd.DataFrame({
        "date": ["2026-01-15", "2026-02-15"]
    })

    result = validate_date_format(df, ["date"])

    assert result["passed"] is True


def test_invalid_date():
    df = pd.DataFrame({
        "date": ["invalid-date"]
    })

    result = validate_date_format(df, ["date"])

    assert result["passed"] is False


# 6. Missing Value Validation
def test_missing_value_validation():
    df = pd.DataFrame({
        "name": ["A", "B"],
        "age": [20, 21]
    })

    result = validate_missing_values(df)

    assert result["passed"] is True


def test_detect_missing_values():
    df = pd.DataFrame({
        "name": ["A", None]
    })

    result = validate_missing_values(df)

    assert result["passed"] is False


# 7. Duplicate Validation
def test_duplicate_validation():
    df = pd.DataFrame({
        "id": [1, 2, 3]
    })

    result = validate_duplicates(df)

    assert result["passed"] is True


def test_detect_duplicates():
    df = pd.DataFrame({
        "id": [1, 1, 2]
    })

    result = validate_duplicates(df)

    assert result["passed"] is False
    assert result["duplicate_count"] == 1


# 8. Anomaly Detection
def test_anomaly_detection():
    df = pd.DataFrame({
        "age": [20, 21, 22, 23, 24, 200]
    })

    result = detect_anomalies(df)

    assert result["passed"] is False
    assert "age" in result["anomalies"]


# 9. Combined Validation
def test_combined_validation():
    df = pd.DataFrame({
        "name": ["A", "B", "C", "D"],
        "age": [20, 21, 22, 23],
        "email": [
            "a@gmail.com",
            "b@gmail.com",
            "c@gmail.com",
            "d@gmail.com"
        ]
    })

    result = run_all_validations(
        df,
        ["name", "age", "email"],
        {
            "name": "object",
            "age": "int64",
            "email": "object"
        },
        {"age": (1, 100)},
        ["email"],
        []
    )

    assert result["total_validations"] == 8
    assert result["overall_passed"] is True
    assert result["data_quality_score"] == 100.0


# 10. JSON Report Generation
def test_save_validation_report(tmp_path):
    report = {
        "overall_passed": True,
        "data_quality_score": 100.0
    }

    output_file = tmp_path / "validation_report.json"

    save_validation_report(report, output_file)

    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8") as file:
        saved_report = json.load(file)

    assert saved_report["overall_passed"] is True
    assert "generated_at" in saved_report


# 11. Missing Input File
def test_missing_dataset_file(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        validate_dataset_file(missing_file)


# 12. Invalid File Extension
def test_invalid_file_extension(tmp_path):
    invalid_file = tmp_path / "data.txt"
    invalid_file.write_text("sample data")

    with pytest.raises(ValueError):
        validate_dataset_file(invalid_file)


# 13. Empty CSV File
def test_empty_csv_file(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")

    with pytest.raises(ValueError):
        validate_dataset_file(empty_file)