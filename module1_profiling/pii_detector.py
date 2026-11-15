import re


def detect_pii_type(column_name, series):
    """
    Identify potentially sensitive information
    using column names and value patterns.
    """

    column = column_name.lower().strip()

    # Email detection
    if "email" in column or "e-mail" in column:
        return {
            "pii_detected": True,
            "pii_type": "EMAIL",
            "confidence": "high",
            "detection_method": "column_name"
        }

    # Phone number detection
    if any(word in column for word in ["phone", "mobile", "contact"]):
        return {
            "pii_detected": True,
            "pii_type": "PHONE_NUMBER",
            "confidence": "high",
            "detection_method": "column_name"
        }

    # Name detection
    if "name" in column:
        return {
            "pii_detected": True,
            "pii_type": "PERSON_NAME",
            "confidence": "high",
            "detection_method": "column_name"
        }

    # Address detection
    if "address" in column:
        return {
            "pii_detected": True,
            "pii_type": "ADDRESS",
            "confidence": "high",
            "detection_method": "column_name"
        }

    # Pattern-based email detection
    values = series.dropna().astype(str)

    if not values.empty:
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        email_matches = values.apply(
            lambda value: bool(re.match(email_pattern, value))
        )

        match_percentage = email_matches.mean()

        if match_percentage >= 0.8:
            return {
                "pii_detected": True,
                "pii_type": "EMAIL",
                "confidence": "high",
                "detection_method": "value_pattern"
            }

    return {
        "pii_detected": False,
        "pii_type": None,
        "confidence": "none",
        "detection_method": "none"
    }