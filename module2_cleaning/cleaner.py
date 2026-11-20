import pandas as pd


def handle_missing_values(df):
    """Handle missing values using median and mode imputation."""

    cleaning_log = []

    for column in df.columns:
        missing_count = int(df[column].isnull().sum())

        if missing_count == 0:
            continue

        if df[column].isnull().all():
            cleaning_log.append({
                "column": column,
                "action": "Skipped",
                "reason": "Column contains only missing values",
                "missing_values": missing_count
            })
            continue

        if pd.api.types.is_numeric_dtype(df[column]):
            fill_value = df[column].median()
            method = "Median"

        else:
            mode_values = df[column].mode(dropna=True)

            if mode_values.empty:
                continue

            fill_value = mode_values.iloc[0]
            method = "Mode"

        df[column] = df[column].fillna(fill_value)

        cleaning_log.append({
            "column": column,
            "action": "Missing values filled",
            "method": method,
            "fill_value": str(fill_value),
            "missing_values": missing_count
        })

    return df, cleaning_log
def remove_duplicate_rows(df):
    """Remove duplicate rows and return the number of removed rows."""

    duplicate_count = int(df.duplicated().sum())

    cleaned_df = df.drop_duplicates().copy()

    cleaning_log = {
        "action": "Duplicate rows removed",
        "duplicates_found": duplicate_count,
        "duplicates_removed": duplicate_count
    }

    return cleaned_df, cleaning_log
def correct_data_types(df):
    """Convert columns into appropriate data types."""

    cleaning_log = []

    for column in df.columns:
        original_type = str(df[column].dtype)

        # Convert date-related columns
        if "date" in column.lower():
            converted = pd.to_datetime(
                df[column],
                errors="coerce",
                format="mixed"
            )

            if converted.notna().any():
                df[column] = converted
                new_type = str(df[column].dtype)

                cleaning_log.append({
                    "column": column,
                    "action": "Date type corrected",
                    "original_type": original_type,
                    "new_type": new_type
                })

        # Convert numeric-looking object columns
        elif df[column].dtype == "object":
            converted = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            if converted.notna().sum() == df[column].notna().sum():
                df[column] = converted

                cleaning_log.append({
                    "column": column,
                    "action": "Numeric type corrected",
                    "original_type": original_type,
                    "new_type": str(df[column].dtype)
                })

    return df, cleaning_log

from pathlib import Path
from module2_cleaning.cleaning_logger import save_cleaning_log


def clean_dataset(
    input_path="Data/raw_dataset.csv",
    output_path="results/cleaned_data.csv"
):
    """Run the complete data cleaning pipeline."""

    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Dataset not found: {input_path}")

    if input_path.suffix.lower() != ".csv":
        raise ValueError("Please provide a CSV file.")
 
    try:
        df = pd.read_csv(input_path)
    except pd.errors.EmptyDataError:
        raise ValueError("The input CSV file is empty.")
    except pd.errors.ParserError:
        raise ValueError("The input CSV file has an invalid format.")

    original_rows = len(df)
    cleaning_log = []

    # Step 1: Handle missing values
    df, missing_log = handle_missing_values(df)
    cleaning_log.extend(missing_log)

    # Step 2: Remove duplicate rows
    df, duplicate_log = remove_duplicate_rows(df)
    cleaning_log.append(duplicate_log)

    # Step 3: Correct data types
    df, type_log = correct_data_types(df)
    cleaning_log.extend(type_log)

    # Save cleaned dataset
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    # Save cleaning log
    log_path = output_file.parent / "cleaning_log.json"
    save_cleaning_log(cleaning_log, output_path=log_path)

    print("\nDATA CLEANING COMPLETED SUCCESSFULLY")
    print("------------------------------------")
    print(f"Original rows: {original_rows}")
    print(f"Cleaned rows: {len(df)}")
    print(f"Rows removed: {original_rows - len(df)}")
    print(f"Remaining missing values: {int(df.isnull().sum().sum())}")
    print(f"Cleaned dataset saved to: {output_file.resolve()}")

    return df, cleaning_log


if __name__ == "__main__":
    clean_dataset()