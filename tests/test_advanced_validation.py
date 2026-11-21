import json
import pandas as pd
import pytest

from module3_validation.validator import (
    validate_column_relationships,
    validate_conditional_rules,
    validate_allowed_values,
    validate_custom_business_rules,
    run_advanced_validations,
    load_validation_rules,
    validate_with_config,
    validate_dataset_with_config,
    run_and_save_advanced_validation,
    print_advanced_validation_summary
)


def test_column_relationships():
    df = pd.DataFrame({
        "minimum_price": [100, 200],
        "maximum_price": [200, 300]
    })

    rules = [{
        "column": "minimum_price",
        "other_column": "maximum_price",
        "operator": "<="
    }]

    result = validate_column_relationships(df, rules)

    assert result[0]["passed"] is True


def test_invalid_column_relationships():
    df = pd.DataFrame({
        "minimum_price": [300, 200],
        "maximum_price": [200, 300]
    })

    rules = [{
        "column": "minimum_price",
        "other_column": "maximum_price",
        "operator": "<="
    }]

    result = validate_column_relationships(df, rules)

    assert result[0]["passed"] is False


def test_conditional_validation():
    df = pd.DataFrame({
        "payment_method": ["UPI", "Card"],
        "transaction_id": ["TX001", None]
    })

    rules = [{
        "condition_column": "payment_method",
        "condition_value": "UPI",
        "target_column": "transaction_id"
    }]

    result = validate_conditional_rules(df, rules)

    assert result[0]["passed"] is True


def test_invalid_conditional_validation():
    df = pd.DataFrame({
        "payment_method": ["UPI", "Card"],
        "transaction_id": [None, "TX002"]
    })

    rules = [{
        "condition_column": "payment_method",
        "condition_value": "UPI",
        "target_column": "transaction_id"
    }]

    result = validate_conditional_rules(df, rules)

    assert result[0]["passed"] is False


def test_allowed_values_validation():
    df = pd.DataFrame({
        "payment_method": ["UPI", "Card", "Cash"]
    })

    rules = [{
        "column": "payment_method",
        "allowed_values": ["UPI", "Card", "Cash"]
    }]

    result = validate_allowed_values(df, rules)

    assert result[0]["passed"] is True


def test_invalid_allowed_values():
    df = pd.DataFrame({
        "payment_method": ["UPI", "Bitcoin"]
    })

    rules = [{
        "column": "payment_method",
        "allowed_values": ["UPI", "Card", "Cash"]
    }]

    result = validate_allowed_values(df, rules)

    assert result[0]["passed"] is False


def test_custom_business_rules():
    df = pd.DataFrame({
        "age": [20, 25, 30]
    })

    rules = [{
        "column": "age",
        "operator": ">=",
        "value": 18
    }]

    result = validate_custom_business_rules(df, rules)

    assert result[0]["passed"] is True


def test_invalid_business_rules():
    df = pd.DataFrame({
        "age": [15, 20, 25]
    })

    rules = [{
        "column": "age",
        "operator": ">=",
        "value": 18
    }]

    result = validate_custom_business_rules(df, rules)

    assert result[0]["passed"] is False


def test_combined_advanced_validation():
    df = pd.DataFrame({
        "minimum_price": [100, 200],
        "maximum_price": [200, 300],
        "payment_method": ["UPI", "Card"],
        "transaction_id": ["TX001", None],
        "age": [20, 25]
    })

    report = run_advanced_validations(
        df,
        relationship_rules=[{
            "column": "minimum_price",
            "other_column": "maximum_price",
            "operator": "<="
        }],
        conditional_rules=[{
            "condition_column": "payment_method",
            "condition_value": "UPI",
            "target_column": "transaction_id"
        }],
        allowed_value_rules=[{
            "column": "payment_method",
            "allowed_values": ["UPI", "Card", "Cash"]
        }],
        business_rules=[{
            "column": "age",
            "operator": ">=",
            "value": 18
        }]
    )

    assert report["total_checks"] == 4
    assert report["passed_checks"] == 4
    assert report["failed_checks"] == 0
    assert report["overall_status"] == "PASSED"


def test_load_validation_rules(tmp_path):
    config_file = tmp_path / "rules.json"

    config_file.write_text(json.dumps({
        "relationship_rules": [],
        "conditional_rules": [],
        "allowed_value_rules": [],
        "business_rules": []
    }))

    rules = load_validation_rules(config_file)

    assert rules["relationship_rules"] == []
    assert rules["business_rules"] == []


def test_missing_configuration_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_validation_rules(tmp_path / "missing.json")


def test_invalid_configuration_structure(tmp_path):
    config_file = tmp_path / "rules.json"
    config_file.write_text(json.dumps([]))

    with pytest.raises(ValueError):
        load_validation_rules(config_file)


def test_validate_with_config(tmp_path):
    df = pd.DataFrame({
        "age": [20, 25]
    })

    config_file = tmp_path / "rules.json"

    config_file.write_text(json.dumps({
        "business_rules": [{
            "column": "age",
            "operator": ">=",
            "value": 18
        }]
    }))

    report = validate_with_config(df, config_file)

    assert report["overall_status"] == "PASSED"
    assert report["total_checks"] == 1


def test_validate_dataset_with_config(tmp_path):
    dataset_file = tmp_path / "data.csv"
    config_file = tmp_path / "rules.json"

    pd.DataFrame({
        "age": [20, 25]
    }).to_csv(dataset_file, index=False)

    config_file.write_text(json.dumps({
        "business_rules": [{
            "column": "age",
            "operator": ">=",
            "value": 18
        }]
    }))

    report = validate_dataset_with_config(
        dataset_file,
        config_file
    )

    assert report["overall_status"] == "PASSED"


def test_advanced_report_generation(tmp_path):
    dataset_file = tmp_path / "data.csv"
    config_file = tmp_path / "rules.json"
    output_file = tmp_path / "advanced_report.json"

    pd.DataFrame({
        "age": [20, 25]
    }).to_csv(dataset_file, index=False)

    config_file.write_text(json.dumps({
        "business_rules": [{
            "column": "age",
            "operator": ">=",
            "value": 18
        }]
    }))

    result = run_and_save_advanced_validation(
        dataset_file,
        config_file,
        output_file
    )

    assert output_file.exists()
    assert result["report"]["overall_status"] == "PASSED"


def test_print_advanced_validation_summary(capsys):
    result = {
        "report": {
            "total_checks": 2,
            "passed_checks": 2,
            "failed_checks": 0,
            "overall_status": "PASSED",
            "results": [
                {
                    "validation": "Age >= 18",
                    "passed": True
                }
            ]
        },
        "saved_path": "results/advanced_validation_report.json"
    }

    print_advanced_validation_summary(result)

    output = capsys.readouterr().out

    assert "ADVANCED DATA VALIDATION REPORT" in output
    assert "PASSED" in output
