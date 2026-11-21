# Advanced Data Validation

## Overview
The Advanced Validation module extends the basic validation system with configurable business rules and advanced data checks.

## Features

1. **Column Relationship Validation:** Compares values between two columns using operators such as <, >, <=, >=, == and !=.
2. **Conditional Validation:** Checks whether a target column contains a value when a specified condition is met.
3. **Allowed Values Validation:** Ensures that a column contains only predefined allowed values.
4. **Custom Business Rules:** Validates data using custom conditions and comparison operators.
5. **JSON Configuration:** Loads validation rules from an external JSON configuration file.
6. **Advanced Validation Report:** Generates a JSON report containing validation results and overall status.

## Configuration

Validation rules are stored in:

`config/validation_rules.json`

The configuration supports four rule categories:

- relationship_rules
- conditional_rules
- allowed_value_rules
- business_rules

## Main Functions

- `validate_column_relationships()`
- `validate_conditional_rules()`
- `validate_allowed_values()`
- `validate_custom_business_rules()`
- `run_advanced_validations()`
- `load_validation_rules()`
- `validate_with_config()`
- `validate_dataset_with_config()`
- `run_and_save_advanced_validation()`
- `print_advanced_validation_summary()`

## Output

The advanced validation report is saved at:

`results/advanced_validation_report.json`

The report contains:
- Total validation checks
- Passed checks
- Failed checks
- Overall validation status
- Individual validation results

## Testing

Advanced validation tests are available in:

`tests/test_advanced_validation.py`

**Advanced validation tests:** 16 passed

**Complete project test suite:** 73 passed

## Conclusion

The Advanced Validation module provides configurable validation rules to identify invalid data and enforce business requirements. It improves the reliability and quality of the cleaned dataset.