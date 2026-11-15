import pandas as pd


def detect_mixed_types(series):
    """
    Detect columns containing mixed numeric and non-numeric values.
    """

    values = series.dropna().astype(str).str.strip()

    if values.empty:
        return {
            "mixed_types_detected": False,
            "numeric_values": 0,
            "non_numeric_values": 0,
            "issue": None
        }

    numeric_mask = pd.to_numeric(
        values,
        errors="coerce"
    ).notna()

    numeric_count = int(numeric_mask.sum())
    non_numeric_count = int((~numeric_mask).sum())

    mixed = numeric_count > 0 and non_numeric_count > 0

    return {
        "mixed_types_detected": mixed,
        "numeric_values": numeric_count,
        "non_numeric_values": non_numeric_count,
        "issue": (
            "Column contains both numeric and non-numeric values"
            if mixed else None
        )
    }