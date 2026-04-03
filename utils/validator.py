"""Validator module for validating library data."""

from datetime import datetime
import re


class Validator:
    """Provides static validation methods."""

    @staticmethod
    def validate_non_empty(value: str) -> bool:
        """Checks that a string is not empty."""
        return bool(value and value.strip())

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validates basic email format."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validates phone number (digits only, 7–15 chars)."""
        return phone.isdigit() and 7 <= len(phone) <= 15

    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Validates date format (YYYY-MM-DD)."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
