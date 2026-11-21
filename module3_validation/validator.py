import re
import json
import pandas as pd
from pathlib import Path
from datetime import datetime


def validate_required_columns(df, required_columns):
    """
    Check whether all required columns exist in the dataset.
    """

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    return {
        "validation": "required_columns",
        "passed": len(missing_columns) == 0,
        "missing_columns": missing_columns
    }
def validate_data_types(df, expected_types):
    """
    Validate whether columns have their expected data types.
    """

    invalid_columns = {}

    for column, expected_type in expected_types.items():

        if column not in df.columns:
            invalid_columns[column] = "Column not found"

        elif str(df[column].dtype) != expected_type:
            invalid_columns[column] = {
                "expected": expected_type,
                "actual": str(df[column].dtype)
            }

    return {
        "validation": "data_types",
        "passed": len(invalid_columns) == 0,
        "invalid_columns": invalid_columns
    }
def validate_numeric_ranges(df, expected_ranges):
    """
    Validate numerical columns against allowed ranges.
    """

    invalid_columns = {}

    for column, (minimum, maximum) in expected_ranges.items():

        if column not in df.columns:
            invalid_columns[column] = "Column not found"
            continue

        if not pd.api.types.is_numeric_dtype(df[column]):
            invalid_columns[column] = "Column is not numeric"
            continue

        invalid_rows = df[
            (df[column] < minimum) |
            (df[column] > maximum)
        ]

        if not invalid_rows.empty:
            invalid_columns[column] = {
                "invalid_count": len(invalid_rows),
                "invalid_values": invalid_rows[column].tolist()
            }

    return {
        "validation": "numeric_ranges",
        "passed": len(invalid_columns) == 0,
        "invalid_columns": invalid_columns
    }

def validate_email_format(df, email_columns):
    """
    Validate email formats while handling missing values separately.
    """

    invalid_emails = {}

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    for column in email_columns:

        if column not in df.columns:
            invalid_emails[column] = "Column not found"
            continue

        email_values = df[column].dropna().astype(str).str.strip()

        valid_mask = email_values.str.match(
            email_pattern,
            na=False
        )

        invalid_values = email_values[~valid_mask]

        if not invalid_values.empty:
            invalid_emails[column] = {
                "invalid_count": len(invalid_values),
                "invalid_values": invalid_values.tolist()
            }

    return {
        "validation": "email_format",
        "passed": len(invalid_emails) == 0,
        "invalid_columns": invalid_emails
    }


def validate_date_format(df, date_columns):
    """
    Validate date values in specified columns.
    """

    invalid_dates = {}

    for column in date_columns:

        if column not in df.columns:
            invalid_dates[column] = "Column not found"
            continue

        converted_dates = pd.to_datetime(
            df[column],
            errors="coerce",
            format="mixed"
        )

        invalid_rows = df[
            df[column].notna() & converted_dates.isna()
        ]

        if not invalid_rows.empty:
            invalid_dates[column] = {
                "invalid_count": len(invalid_rows),
                "invalid_values": invalid_rows[column].tolist()
            }

    return {
        "validation": "date_format",
        "passed": len(invalid_dates) == 0,
        "invalid_columns": invalid_dates
    }

def validate_missing_values(df, allowed_missing=0):
    """
    Check whether columns contain excessive missing values.
    """

    missing_values = df.isnull().sum()
    invalid_columns = {}

    for column, count in missing_values.items():
        if count > allowed_missing:
            invalid_columns[column] = int(count)

    return {
        "validation": "missing_values",
        "passed": len(invalid_columns) == 0,
        "invalid_columns": invalid_columns
    }


def validate_duplicates(df):
    """
    Check whether the dataset contains duplicate rows.
    """

    duplicate_count = int(df.duplicated().sum())

    return {
        "validation": "duplicate_records",
        "passed": duplicate_count == 0,
        "duplicate_count": duplicate_count
    }

def detect_anomalies(df):
    """
    Detect numerical anomalies using the IQR method.
    """

    anomalies = {}

    numeric_columns = df.select_dtypes(include=["number"]).columns

    for column in numeric_columns:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_limit = Q1 - 1.5 * IQR
        upper_limit = Q3 + 1.5 * IQR

        outliers = df[
            (df[column] < lower_limit) |
            (df[column] > upper_limit)
        ]

        if not outliers.empty:
            anomalies[column] = {
                "outlier_count": len(outliers),
                "outlier_values": outliers[column].tolist(),
                "lower_limit": lower_limit,
                "upper_limit": upper_limit
            }

    return {
        "validation": "anomaly_detection",
        "passed": len(anomalies) == 0,
        "anomalies": anomalies
    }

def run_all_validations(
    df,
    required_columns,
    expected_types,
    expected_ranges,
    email_columns,
    date_columns,
    allowed_missing=0
):
    """Run all validation checks and generate a combined report."""

    results = [
        validate_required_columns(df, required_columns),
        validate_data_types(df, expected_types),
        validate_numeric_ranges(df, expected_ranges),
        validate_email_format(df, email_columns),
        validate_date_format(df, date_columns),
        validate_missing_values(df, allowed_missing),
        validate_duplicates(df),
        detect_anomalies(df)
    ]

    total = len(results)
    passed = sum(result["passed"] for result in results)
    failed = total - passed

    quality_score = round((passed / total) * 100, 2) if total else 0

    return {
        "overall_passed": failed == 0,
        "total_validations": total,
        "passed_validations": passed,
        "failed_validations": failed,
        "data_quality_score": quality_score,
        "validation_results": results
    }

def save_validation_report(report, output_path="results/validation_report.json"):
    """
    Save validation results with execution metadata.
    """

    report["generated_at"] = datetime.now().isoformat()
    report["report_type"] = "Data Validation Report"

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, default=str)

    print(f"Validation report saved to: {output_file.resolve()}")

    return output_file

def validate_dataset_file(
    input_path="results/cleaned_data.csv",
    output_path="results/validation_report.json"
):
    """
    Load a cleaned dataset, validate it, and save the report.
    """

    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(
            f"Dataset not found: {input_file}"
    )

    if not input_file.is_file():
        raise ValueError("Input path must be a file.")

    if input_file.suffix.lower() != ".csv":
        raise ValueError("Input file must be a CSV file.")

    try:
        df = pd.read_csv(input_file)

    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty.")

    except pd.errors.ParserError:
        raise ValueError("The CSV file has an invalid format.")

    except UnicodeDecodeError:
        raise ValueError("The CSV file has an encoding issue.")

    if len(df.columns) == 0:
        raise ValueError("The CSV file has no columns.")

    required_columns = [
        "customer_id",
        "customer_name",
        "email",
        "age",
        "city",
        "purchase_date",
        "product",
        "quantity",
        "price",
        "payment_method"
    ]

    expected_types = {
        "customer_id": "object",
        "customer_name": "object",
        "email": "object",
        "age": "float64",
        "city": "object",
        "product": "object",
        "quantity": "int64",
        "price": "int64",
        "payment_method": "object"
    }

    expected_ranges = {
        "age": (1, 100),
        "quantity": (1, 1000),
        "price": (0, 100000)
    }

    report = run_all_validations(
        df,
        required_columns,
        expected_types,
        expected_ranges,
        ["email"],
        ["purchase_date"]
    )

    save_validation_report(report, output_path)

    returnreport


if __name__ == "__main__":

    try:
        report = validate_dataset_file()

        print("\nDATA VALIDATION COMPLETED")
        print("-------------------------")

        print(
            f"Total Validations: {report['total_validations']}"
        )

        print(
            f"Passed: {report['passed_validations']}"
        )

        print(
            f"Failed: {report['failed_validations']}"
        )

        print(
            f"Data Quality Score: {report['data_quality_score']}%"
        )

        print(
            f"Overall Status: "
            f"{'PASSED' if report['overall_passed'] else 'FAILED'}"
        )

    except (FileNotFoundError, ValueError) as error:
        print(f"VALIDATION ERROR: {error}")