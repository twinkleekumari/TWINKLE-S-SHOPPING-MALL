import re

def validate_phone(phone_str: str) -> bool:
    """Validates 10-digit phone number format."""
    return bool(re.match(r"^\d{10}$", phone_str.strip()))

def validate_email(email_str: str) -> bool:
    """Validates basic email format."""
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email_str.strip()))
