import json
import re
from pathlib import Path
from collections import Counter

import pandas as pd


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "Data" / "raw_dataset.csv"

OUTPUT_PATH = PROJECT_ROOT / "results" / "profiling_report.json"


# --------------------------------------------------
# SEMANTIC COLUMN DETECTION
# --------------------------------------------------

def detect_semantic_type(column_name, series):
    """Infer the likely meaning of a column."""

    name = column_name.lower().strip()

    if "email" in name or "e_mail" in name:
        return "email"

    if "phone" in name or "mobile" in name or "telephone" in name:
        return "phone"

    if name == "age" or name.endswith("_age"):
        return "age"

    if "date" in name or name.endswith("_at"):
        return "date"

    if name == "id" or name.endswith("_id"):
        return "identifier"

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"

    return "categorical"


# --------------------------------------------------
# SUSPICIOUS VALUE DETECTION
# --------------------------------------------------

def detect_suspicious_values(column_name, series):
    """Find potential issues using basic, explainable rules."""

    issues = []
    name = column_name.lower().strip()

    # Check age values.
    if name == "age" or name.endswith("_age"):
        numeric_values = pd.to_numeric(series, errors="coerce")

        invalid_age = (
            numeric_values.notna()
            & ((numeric_values < 0) | (numeric_values > 120))
        )

        for index in series[invalid_age].index:
            issues.append({
                "row": int(index) + 2,
                "value": str(series.loc[index]),
                "issue": "Age outside the expected range 0-120",
                "severity": "warning"
            })

    # Check email format.
    if "email" in name or "e_mail" in name:
        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        for index, value in series.items():
            if pd.isna(value) or str(value).strip() == "":
                continue

            if not re.fullmatch(email_pattern, str(value).strip()):
                issues.append({
                    "row": int(index) + 2,
                    "value": str(value),
                    "issue": "Potentially invalid email format",
                    "severity": "warning"
                })

    # Check negative quantities and prices.
    if name in {"quantity", "price", "amount", "total_amount"}:
        numeric_values = pd.to_numeric(series, errors="coerce")

        invalid_values = numeric_values.notna() & (numeric_values < 0)

        for index in series[invalid_values].index:
            issues.append({
                "row": int(index) + 2,
                "value": str(series.loc[index]),
                "issue": "Negative value detected",
                "severity": "warning"
            })

    return issues


# --------------------------------------------------
# DATE FORMAT ANALYSIS
# --------------------------------------------------

def analyze_date_formats(series):
    """Count common date-format patterns without modifying values."""

    patterns = {
        "YYYY-MM-DD": r"^\d{4}-\d{2}-\d{2}$",
        "YYYY/MM/DD": r"^\d{4}/\d{2}/\d{2}$",
        "DD-MM-YYYY": r"^\d{2}-\d{2}-\d{4}$",
        "DD/MM/YYYY": r"^\d{2}/\d{2}/\d{4}$",
    }

    counts = Counter()
    unrecognized_count = 0

    for value in series.dropna():
        text = str(value).strip()

        matched = False

        for format_name, pattern in patterns.items():
            if re.fullmatch(pattern, text):
                counts[format_name] += 1
                matched = True
                break

        if not matched:
            unrecognized_count += 1

    return {
        "format_counts": dict(counts),
        "unrecognized_format_count": unrecognized_count,
        "has_multiple_formats": len(counts) > 1
    }


# --------------------------------------------------
# DATASET PROFILING
# --------------------------------------------------

def profile_dataset(file_path):
    """Generate a detailed profiling report for a CSV dataset."""

    df = pd.read_csv(file_path)

    report = {
        "dataset_name": Path(file_path).name,
        "total_rows": int(df.shape[0]),
        "total_columns": int(df.shape[1]),
        "duplicate_rows": int(df.duplicated().sum()),
        "total_missing_values": int(df.isnull().sum().sum()),
        "columns": {},
        "data_quality_warnings": []
    }

    for column in df.columns:
        series = df[column]

        semantic_type = detect_semantic_type(column, series)

        column_report = {
            "data_type": str(series.dtype),
            "semantic_type": semantic_type,
            "missing_values": int(series.isnull().sum()),
            "missing_percentage": round(
                float(series.isnull().mean() * 100), 2
            ),
            "unique_values": int(series.nunique(dropna=True)),
            "suspicious_values": detect_suspicious_values(column, series)
        }

        # Numeric statistics.
        if pd.api.types.is_numeric_dtype(series):
            column_report["statistics"] = {
                "minimum": (
                    float(series.min())
                    if series.notna().any()
                    else None
                ),
                "maximum": (
                    float(series.max())
                    if series.notna().any()
                    else None
                ),
                "mean": (
                    round(float(series.mean()), 2)
                    if series.notna().any()
                    else None
                ),
                "median": (
                    float(series.median())
                    if series.notna().any()
                    else None
                )
            }

        # Most frequent values for categorical columns.
        if semantic_type == "categorical":
            frequencies = series.value_counts(dropna=True)

            column_report["top_values"] = [
                {
                    "value": str(value),
                    "count": int(count)
                }
                for value, count in frequencies.head(5).items()
            ]

        # Date-format checks.
        if semantic_type == "date":
            column_report["date_format_analysis"] = analyze_date_formats(
                series
            )

            if column_report["date_format_analysis"]["has_multiple_formats"]:
                report["data_quality_warnings"].append({
                    "column": column,
                    "issue": "Multiple date formats detected",
                    "severity": "warning"
                })

        # Add warnings for missing values.
        if column_report["missing_values"] > 0:
            report["data_quality_warnings"].append({
                "column": column,
                "issue": "Missing values detected",
                "count": column_report["missing_values"],
                "severity": "warning"
            })

        # Add suspicious-value warnings.
        if column_report["suspicious_values"]:
            report["data_quality_warnings"].append({
                "column": column,
                "issue": "Suspicious values detected",
                "count": len(column_report["suspicious_values"]),
                "severity": "warning"
            })

        report["columns"][column] = column_report

    # Duplicate-row warning.
    if report["duplicate_rows"] > 0:
        report["data_quality_warnings"].append({
            "issue": "Duplicate rows detected",
            "count": report["duplicate_rows"],
            "severity": "warning"
        })

    return report


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------

def main():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    report = profile_dataset(DATASET_PATH)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print("\nDATA PROFILING COMPLETED SUCCESSFULLY")
    print("-------------------------------------")
    print(f"Dataset: {report['dataset_name']}")
    print(f"Rows: {report['total_rows']}")
    print(f"Columns: {report['total_columns']}")
    print(f"Missing values: {report['total_missing_values']}")
    print(f"Duplicate rows: {report['duplicate_rows']}")
    print(f"Quality warnings: {len(report['data_quality_warnings'])}")
    print(f"\nReport saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()