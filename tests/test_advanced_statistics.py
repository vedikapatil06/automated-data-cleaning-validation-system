import pandas as pd

from module1_profiling.advanced_statistics import (
    calculate_numeric_statistics,
    detect_iqr_outliers,
    calculate_cardinality,
)


def test_numeric_statistics():
    series = pd.Series([10, 20, 30, 40, 50])

    result = calculate_numeric_statistics(series)

    assert result["count"] == 5
    assert result["mean"] == 30.0
    assert result["median"] == 30.0
    assert result["minimum"] == 10.0
    assert result["maximum"] == 50.0
    assert result["q1"] == 20.0
    assert result["q3"] == 40.0
    assert result["iqr"] == 20.0


def test_iqr_outlier_detection():
    series = pd.Series([10, 11, 12, 13, 14, 100])

    result = detect_iqr_outliers(series)

    assert len(result) == 1
    assert result[0]["value"] == 100.0


def test_cardinality():
    series = pd.Series(["Pune", "Mumbai", "Pune", "Sangli"])

    result = calculate_cardinality(series)

    assert result["total_non_null_values"] == 4
    assert result["unique_values"] == 3
    assert result["uniqueness_percentage"] == 75.0