# Module 4: Automated Data Processing Pipeline

## 1. Overview

The Automated Data Processing Pipeline integrates data profiling, data cleaning, basic validation, and advanced validation into a single automated workflow.

It reduces manual effort and provides a structured process for improving and evaluating dataset quality.

## 2. Project Structure

```text
module4_pipeline/
    __init__.py
    pipeline.py

tests/
    test_pipeline.py
```

## 3. Pipeline Workflow

The pipeline executes four main stages:

### Step 1: Data Profiling
- Analyzes the input dataset.
- Identifies missing values and duplicate records.
- Generates a profiling report.
- Saves the report as `profiling_report.json`.

### Step 2: Data Cleaning
- Handles missing values.
- Removes duplicate records.
- Corrects data types.
- Standardizes text values.
- Handles outliers.
- Saves the cleaned dataset and cleaning log.

### Step 3: Basic Data Validation
- Checks required columns.
- Validates data types.
- Checks numeric ranges.
- Validates email and date formats.
- Detects missing values, duplicates, and anomalies.
- Generates `validation_report.json`.

### Step 4: Advanced Data Validation
- Checks column relationships.
- Validates conditional rules.
- Checks allowed values.
- Applies custom business rules.
- Generates `advanced_validation_report.json`.

## 4. Pipeline Execution

Activate the virtual environment and execute:

```bash
python -m module4_pipeline.pipeline
```

The pipeline processes the input dataset and generates the required reports automatically.

## 5. Generated Output Files

The pipeline generates the following files inside the `results/` directory:

| File | Description |
|---|---|
| profiling_report.json | Dataset profiling results |
| cleaned_data.csv | Cleaned dataset |
| cleaning_log.json | Cleaning operation details |
| validation_report.json | Basic validation results |
| advanced_validation_report.json | Advanced validation results |
| pipeline_summary.json | Overall pipeline execution summary |

## 6. Testing

Pipeline integration is tested using pytest.

Run the pipeline test:

```bash
python -m pytest tests/test_pipeline.py -v
```

Run all project tests:

```bash
python -m pytest -v
```

Latest test result: **74 tests passed.**

## 7. Conclusion

Module 4 successfully integrates all major project components into one automated data processing workflow. It generates profiling, cleaning, and validation reports and provides a consolidated pipeline summary.