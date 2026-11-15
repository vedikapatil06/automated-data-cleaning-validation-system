import pandas as pd

from module1_profiling.pii_detector import detect_pii_type


def test_email_detection():
    series = pd.Series([
        "user1@example.com",
        "user2@example.com"
    ])

    result = detect_pii_type("email", series)

    assert result["pii_detected"] is True
    assert result["pii_type"] == "EMAIL"


def test_phone_detection():
    series = pd.Series([
        "9876543210",
        "8765432109"
    ])

    result = detect_pii_type("phone_number", series)

    assert result["pii_detected"] is True
    assert result["pii_type"] == "PHONE_NUMBER"


def test_name_detection():
    series = pd.Series([
        "Rahul",
        "Priya"
    ])

    result = detect_pii_type("customer_name", series)

    assert result["pii_detected"] is True
    assert result["pii_type"] == "PERSON_NAME"


def test_non_pii_detection():
    series = pd.Series([100, 200, 300])

    result = detect_pii_type("quantity", series)

    assert result["pii_detected"] is False