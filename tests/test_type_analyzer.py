import pandas as pd

from module1_profiling.type_analyzer import detect_mixed_types


def test_mixed_numeric_and_text():
    series = pd.Series(["100", "200", "invalid", "300"])

    result = detect_mixed_types(series)

    assert result["mixed_types_detected"] is True
    assert result["numeric_values"] == 3
    assert result["non_numeric_values"] == 1


def test_only_numeric_values():
    series = pd.Series(["100", "200", "300"])

    result = detect_mixed_types(series)

    assert result["mixed_types_detected"] is False


def test_only_text_values():
    series = pd.Series(["Pune", "Mumbai", "Sangli"])

    result = detect_mixed_types(series)

    assert result["mixed_types_detected"] is False


def test_empty_column():
    series = pd.Series([None, None])

    result = detect_mixed_types(series)

    assert result["mixed_types_detected"] is False