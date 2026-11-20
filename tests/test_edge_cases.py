import pandas as pd
import pytest

from module1_profiling.profiler import profile_dataset
from module1_profiling.advanced_statistics import (
    calculate_numeric_statistics,
    detect_iqr_outliers,
    calculate_cardinality,
)


def test_empty_dataset_with_headers(tmp_path):
    """Test profiling a CSV containing headers but no data rows."""

    data = pd.DataFrame(columns=["customer_id", "age"])

    file_path = tmp_path / "empty.csv"
    data.to_csv(file_path, index=False)

    report = profile_dataset(file_path)

    assert report["total_rows"] == 0
    assert report["total_columns"] == 2
    assert report["total_missing_values"] == 0


def test_column_with_only_missing_values(tmp_path):
    """Test a column containing only missing values."""

    data = pd.DataFrame({
        "age": [None, None, None]
    })

    file_path = tmp_path / "missing.csv"
    data.to_csv(file_path, index=False)

    report = profile_dataset(file_path)

    assert report["columns"]["age"]["missing_values"] == 3
    assert report["columns"]["age"]["cardinality"]["unique_values"] == 0


def test_all_rows_are_duplicates(tmp_path):
    """Test a dataset where all rows contain identical values."""

    data = pd.DataFrame({
        "customer_id": ["C001", "C001", "C001"],
        "age": [25, 25, 25]
    })

    file_path = tmp_path / "all_duplicates.csv"
    data.to_csv(file_path, index=False)

    report = profile_dataset(file_path)

    assert report["duplicate_rows"] == 2


def test_invalid_numeric_values():
    """Test statistics when a column contains invalid numeric values."""

    values = pd.Series(["10", "20", "invalid", "30"])

    result = calculate_numeric_statistics(values)

    assert result["count"] == 3
    assert result["mean"] == 20.0


def test_outlier_detection_with_missing_values():
    """Test IQR detection when some values are missing."""

    values = pd.Series([10, 12, 14, 15, 16, 100, None])

    result = detect_iqr_outliers(values)

    assert len(result) == 1
    assert result[0]["value"] == 100.0


def test_cardinality_for_empty_column():
    """Test cardinality calculation for an empty column."""

    values = pd.Series([None, None, None])

    result = calculate_cardinality(values)

    assert result["total_non_null_values"] == 0
    assert result["unique_values"] == 0
    assert result["uniqueness_percentage"] == 0.0


def test_nonexistent_csv_file():
    """Test error handling for a missing CSV file."""

    file_path = "nonexistent_dataset.csv"

    with pytest.raises(FileNotFoundError):
        profile_dataset(file_path)