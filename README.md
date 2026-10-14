# Automated Data Cleaning & Validation System

## Project Overview

This project is an automated data quality system that profiles,
cleans, validates, and detects anomalies in datasets.

## Project Domain

Retail / E-commerce

## Objectives

- Profile datasets automatically
- Detect missing and inconsistent data
- Clean and transform datasets
- Validate data using rules
- Detect anomalies
- Generate data quality reports
- Provide an automated end-to-end pipeline

## Technology Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- SciPy
- Matplotlib
- Seaborn
- PyYAML
- Pytest
- Docker
- GitHub

## Project Modules

1. Advanced Data Profiling & Metadata Intelligence
2. Advanced Data Cleaning & Transformation Pipeline
3. AI Validation, Anomaly Detection & Rule Engine
4. Integration, Orchestration & Production Engineering

## Project Status

Sprint 1 - Project Setup and Dataset Selection


## Sprint 2: Data Profiling Module

### Overview
Implemented the initial data profiling module for the Automated Data Cleaning & Validation System.

### Features
- CSV dataset loading and analysis
- Row and column counts
- Missing-value detection and percentages
- Duplicate-row detection
- Data type and semantic column detection
- Numeric statistics
- Suspicious age and email detection
- Date-format inconsistency detection
- Categorical value summaries
- JSON profiling report generation

### Output
The profiling report is saved to:
`results/profiling_report.json`

### Automated Testing
Automated tests are implemented using pytest.

Test coverage includes:
- Semantic type detection
- Missing-value detection
- Duplicate-row detection
- Invalid email detection
- Suspicious age detection
- Multiple date-format detection

Latest test result: **6 passed**.

### How to Run
Activate the virtual environment and execute:

```bash
python module1_profiling/profiler.py