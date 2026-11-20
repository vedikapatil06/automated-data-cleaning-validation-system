# Module 1: Advanced Data Profiling and Metadata Intelligence

## 1. Overview

Module 1 is responsible for analyzing datasets and generating detailed profiling reports. It identifies data quality issues, understands column types, detects sensitive information, and calculates statistical information.

The module helps users understand their dataset before performing data cleaning and validation.

## 2. Features

### 2.1 Basic Data Profiling
- Counts total rows and columns.
- Detects duplicate records.
- Identifies missing values.
- Calculates missing value percentages.

### 2.2 Semantic Type Detection
Identifies the meaning of columns, such as:
- Age
- Email
- Date
- Identifier
- Numeric
- Categorical

### 2.3 Advanced Statistical Analysis
Calculates:
- Mean
- Median
- Standard deviation
- Minimum and maximum
- First and third quartiles
- Interquartile range (IQR)

### 2.4 Outlier Detection
Uses the Interquartile Range (IQR) method to identify unusually high or low numeric values.

### 2.5 PII Detection
Identifies potentially sensitive information, including:
- Email addresses
- Phone numbers
- Person names
- Addresses

The detector reports PII categories without returning actual sensitive values.

### 2.6 Mixed Data Type Detection
Identifies columns containing a mixture of numeric and non-numeric values.

### 2.7 Cardinality Analysis
Calculates the number of unique and non-null values in each column.

### 2.8 Suspicious Value Detection
Identifies potentially invalid values, such as:
- Invalid email addresses
- Unreasonable ages
- Negative quantities or prices

### 2.9 Date Format Analysis
Detects different date formats within a column and identifies inconsistent formats.

## 3. Technologies Used

- Python
- Pandas
- NumPy
- Pytest
- JSON

## 4. Project Structure

```text
module1_profiling/
    __init__.py
    profiler.py
    advanced_statistics.py
    pii_detector.py
    type_analyzer.py

tests/
    test_profiler.py
    test_advanced_statistics.py
    test_pii_detector.py
    test_type_analyzer.py
    test_edge_cases.py

results/
    profiling_report.json
```

## 5. How to Run the Module

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Run the profiling module:

```powershell
python -m module1_profiling.profiler
```

The generated profiling report is saved in:

```text
results/profiling_report.json
```

## 6. Testing

Run the complete test suite:

```powershell
python -m pytest tests -v
```

The project includes tests for:
- Basic profiling
- Statistical calculations
- PII detection
- Mixed data type detection
- Empty datasets
- Missing values
- Duplicate records
- Invalid numeric values
- Missing CSV files

## 7. Error Handling

The module handles common file-related errors, including:
- Missing dataset files
- Invalid file formats
- Empty CSV files
- Invalid or corrupted CSV data
- Unsupported text encoding

## 8. Conclusion

Module 1 provides advanced data profiling and metadata intelligence. It combines statistical analysis, data quality checks, PII detection, and type analysis to generate a detailed JSON profiling report.

This module establishes the foundation for the next stages of the Automated Data Cleaning and Validation System.