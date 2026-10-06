import re


def clean_text(text):
    return re.sub(r"\s+", " ", str(text)).strip()


def validate_name(name):
    name = clean_text(name)
    if not name:
        return False, "Name cannot be empty."
    if not re.fullmatch(r"[A-Za-z][A-Za-z\s'-]{1,49}", name):
        return False, "Use letters, spaces, hyphens or apostrophes only."
    return True, name


def validate_region(region):
    region = clean_text(region)
    if not region:
        return False, "Location cannot be empty."
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9\s,'-]{1,59}", region):
        return False, "Location contains invalid characters."
    return True, region


def validate_positive_number(value, field_name="Value"):
    try:
        number = float(value)
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid number."
    if number <= 0:
        return False, f"{field_name} must be greater than zero."
    return True, number
