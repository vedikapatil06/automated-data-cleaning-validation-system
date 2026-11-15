import pandas as pd


def calculate_numeric_statistics(series):
    """
    Calculate detailed statistics for a numeric column.
    """

    numeric_series = pd.to_numeric(series, errors="coerce").dropna()

    if numeric_series.empty:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "standard_deviation": None,
            "minimum": None,
            "maximum": None,
            "q1": None,
            "q3": None,
            "iqr": None,
        }

    q1 = numeric_series.quantile(0.25)
    q3 = numeric_series.quantile(0.75)

    return {
        "count": int(numeric_series.count()),
        "mean": round(float(numeric_series.mean()), 2),
        "median": round(float(numeric_series.median()), 2),
        "standard_deviation": round(float(numeric_series.std()), 2),
        "minimum": round(float(numeric_series.min()), 2),
        "maximum": round(float(numeric_series.max()), 2),
        "q1": round(float(q1), 2),
        "q3": round(float(q3), 2),
        "iqr": round(float(q3 - q1), 2),
    }


def detect_iqr_outliers(series):
    """
    Detect numerical outliers using the IQR method.

    Values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR
    are considered potential outliers.
    """

    numeric_series = pd.to_numeric(series, errors="coerce")

    valid_values = numeric_series.dropna()

    if valid_values.empty:
        return []

    q1 = valid_values.quantile(0.25)
    q3 = valid_values.quantile(0.75)
    iqr = q3 - q1

    lower_limit = q1 - (1.5 * iqr)
    upper_limit = q3 + (1.5 * iqr)

    outliers = []

    for index, value in numeric_series.items():
        if pd.isna(value):
            continue

        if value < lower_limit or value > upper_limit:
            outliers.append({
                "row": int(index) + 2,
                "value": float(value),
                "lower_limit": round(float(lower_limit), 2),
                "upper_limit": round(float(upper_limit), 2),
            })

    return outliers


def calculate_cardinality(series):
    """
    Calculate uniqueness/cardinality information for a column.
    """

    total_values = int(series.notna().sum())
    unique_values = int(series.nunique(dropna=True))

    if total_values == 0:
        uniqueness_percentage = 0.0
    else:
        uniqueness_percentage = round(
            (unique_values / total_values) * 100,
            2
        )

    return {
        "total_non_null_values": total_values,
        "unique_values": unique_values,
        "uniqueness_percentage": uniqueness_percentage,
    }