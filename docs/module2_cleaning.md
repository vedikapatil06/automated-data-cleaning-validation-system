# Module 2: Data Cleaning

## 1. Overview

The Data Cleaning Module is responsible for improving dataset quality by identifying and handling missing values, duplicate records, incorrect data types, inconsistent text values, and numerical outliers.

It takes the raw dataset as input and generates a cleaned dataset along with a cleaning log.

## 2. Objectives

- Handle missing values.
- Remove duplicate records.
- Correct incorrect data types.
- Standardize text values.
- Detect and treat numerical outliers.
- Maintain a log of cleaning operations.
- Save the cleaned dataset.

## 3. Project Files

The module contains the following files:

- `cleaner.py` – Contains the main data cleaning functions.
- `cleaning_logger.py` – Records and saves cleaning operations.
- `test_cleaning.py` – Contains unit tests for the cleaning module.

## 4. Cleaning Functions

### 4.1 Handle Missing Values

Function: `handle_missing_values(df)`

- Identifies missing values in the dataset.
- Fills missing numerical values using the median.
- Fills missing text values using the mode.
- Skips columns where all values are missing.
- Records the operations in the cleaning log.

### 4.2 Remove Duplicate Rows

Function: `remove_duplicate_rows(df)`

- Identifies duplicate records.
- Removes duplicate rows.
- Records the number of removed rows.

### 4.3 Correct Data Types

Function: `correct_data_types(df)`

- Identifies columns with incorrect data types.
- Converts date columns into datetime format.
- Converts numeric-looking text columns into numeric values.
- Records successful type corrections.

### 4.4 Standardize Text Values

Function: `standardize_text_values(df)`

- Removes leading and trailing spaces.
- Replaces multiple spaces with a single space.
- Converts selected text columns into title case.
- Preserves email formatting and missing values.
- Records the number of changed values.

### 4.5 Handle Numerical Outliers

Function: `handle_outliers(df)`

- Detects outliers using the Interquartile Range (IQR) method.
- Calculates Q1, Q3, and IQR.
- Determines lower and upper limits.
- Caps values outside the limits.
- Records the number of treated outliers.

## 5. Cleaning Pipeline

Function: `clean_dataset(input_path, output_path)`

The main cleaning pipeline performs the following operations:

1. Reads the raw CSV dataset.
2. Handles missing values.
3. Removes duplicate rows.
4. Standardizes text values.
5. Corrects data types.
6. Handles numerical outliers.
7. Saves the cleaned dataset.
8. Generates a cleaning log.

## 6. Cleaning Log

The cleaning logger is implemented in `cleaning_logger.py`.

It records:

- Date and time of execution.
- Total number of cleaning operations.
- Details of each operation.
- Number of affected values or rows.

The log is saved as `cleaning_log.json` in the output directory.

## 7. Output Files

After successful execution, the module generates:

- `results/cleaned_data.csv` – Final cleaned dataset.
- `results/cleaning_log.json` – Record of cleaning operations.

The original raw dataset remains unchanged.

## 8. Testing

Unit tests are implemented using the Pytest framework.

The tests cover:

- Missing value handling.
- Duplicate removal.
- Data type correction.
- Empty-column handling.
- Custom output paths.
- Missing and empty input files.
- Cleaning log generation.
- Text standardization.
- Text capitalization.
- Email formatting preservation.
- Missing value preservation during text standardization.
- Outlier treatment.
- Dataset without outliers.

**Test Result:** 13 tests passed successfully.

## 9. Execution

Run the cleaning module from the project root directory:

```bash
python -m module2_cleaning.cleaner
```

Run the cleaning tests:

```bash
python -m pytest tests/test_cleaning.py -v
```

## 10. Conclusion

The Data Cleaning Module successfully automates important data preparation operations. It improves dataset consistency, handles common data quality issues, treats numerical outliers, and maintains a record of cleaning activities. The module is tested and integrated into the project.