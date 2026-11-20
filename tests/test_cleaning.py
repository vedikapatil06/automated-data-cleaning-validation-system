import pandas as pd
import pytest



from module2_cleaning.cleaner import(
    handle_missing_values,
    remove_duplicate_rows,
    correct_data_types,
    clean_dataset,
    standardize_text_values,
    handle_outliers
)


def test_missing_value_handling():
    df = pd.DataFrame({
        "age": [20, None, 30],
        "city": ["Pune", None, "Mumbai"]
    })

    cleaned_df, log = handle_missing_values(df)

    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df["age"].iloc[1] == 25
    assert cleaned_df["city"].iloc[1] == "Mumbai"
    assert len(log) == 2


def test_duplicate_removal():
    df = pd.DataFrame({
        "name": ["A", "B", "A"],
        "age": [20, 25, 20]
    })

    cleaned_df, log = remove_duplicate_rows(df)

    assert len(cleaned_df) == 2
    assert log["duplicates_removed"] == 1


def test_data_type_correction():
    df = pd.DataFrame({
        "quantity": ["10", "20", "30"],
        "purchase_date": ["2026-01-10", "2026/01/11", "2026-01-12"]
    })

    cleaned_df, log = correct_data_types(df)

    assert pd.api.types.is_numeric_dtype(cleaned_df["quantity"])
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df["purchase_date"])
    assert len(log) == 2


def test_empty_column_missing_values():
    df = pd.DataFrame({
        "age": [None, None, None]
    })

    cleaned_df, log = handle_missing_values(df)

    assert cleaned_df["age"].isnull().all()
    assert log[0]["action"] == "Skipped"


def test_cleaning_pipeline(tmp_path):
    data = pd.DataFrame({
        "customer": ["A", "B", "B"],
        "age": [20, None, None]
    })

    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "cleaned.csv"
    log_file = tmp_path / "cleaning_log.json"

    data.to_csv(input_file, index=False)

    cleaned_df, log = clean_dataset(
        input_path=input_file,
        output_path=output_file
    )

    assert output_file.exists()
    assert log_file.exists()
    assert len(cleaned_df) == 2
    assert cleaned_df.isnull().sum().sum() == 0


def test_missing_input_file():
    with pytest.raises(FileNotFoundError):
        clean_dataset("missing_dataset.csv")



def test_empty_csv_file(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")

    with pytest.raises(ValueError, match="input CSV file is empty"):
        clean_dataset(input_path=empty_file)



def test_text_standardization():
    df = pd.DataFrame({
        "name": ["  Vedika  ", " Rahul", "Priya   Patil "],
        "city": [" Pune ", "Mumbai  ", " Sangli"]
    })

    cleaned_df, log = standardize_text_values(df)

    assert cleaned_df["name"].tolist() == [
        "Vedika", "Rahul", "Priya Patil"
    ]

    assert cleaned_df["city"].tolist() == [
        "Pune", "Mumbai", "Sangli"
    ]

    assert len(log) == 2

def test_text_capitalization():
    df = pd.DataFrame({
        "city": ["pune", "MUMBAI", "sangli"],
        "customer_name": ["vedika patil", "RAHUL", "priya"]
    })

    cleaned_df, log = standardize_text_values(df)

    assert cleaned_df["city"].tolist() == [
        "Pune", "Mumbai", "Sangli"
    ]

    assert cleaned_df["customer_name"].tolist() == [
        "Vedika Patil", "Rahul", "Priya"
    ]

def test_email_format_preserved():
    df = pd.DataFrame({
        "email": ["  Vedika@Gmail.com  ", " Rahul@Yahoo.com "]
    })

    cleaned_df, log = standardize_text_values(df)

    assert cleaned_df["email"].tolist() == [
        "Vedika@Gmail.com",
        "Rahul@Yahoo.com"
    ]

def test_text_standardization_with_missing_values():
    df = pd.DataFrame({
        "city": [" pune ", None, "mumbai"],
        "email": ["test@gmail.com", None, "user@yahoo.com"]
    })

    cleaned_df, log = standardize_text_values(df)

    assert cleaned_df["city"].iloc[0] == "Pune"
    assert pd.isna(cleaned_df["city"].iloc[1])
    assert cleaned_df["city"].iloc[2] == "Mumbai"

    assert pd.isna(cleaned_df["email"].iloc[1])


def test_outlier_treatment():
    df = pd.DataFrame({
        "age": [20, 22, 21, 23, 24, 200]
    })

    cleaned_df, log = handle_outliers(df)

    assert cleaned_df["age"].max() < 200
    assert len(log) == 1
    assert log[0]["outliers_treated"] == 1


def test_no_outliers():
    df = pd.DataFrame({
        "age": [20, 21, 22, 23, 24]
    })

    cleaned_df, log = handle_outliers(df)

    assert cleaned_df["age"].tolist() == [20, 21, 22, 23, 24]
    assert len(log) == 0