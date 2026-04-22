"""Validator module for validating library data."""

from datetime import datetime
import re


class Validator:
    """Provides static validation methods."""

    @staticmethod
    def validate_name(name: str) -> bool:
        """Validates member name: non-empty, max 50 characters."""
        return bool(name and name.strip()) and len(name.strip()) <= 50

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

    @staticmethod
    def validate_faculty(faculty: str) -> bool:
        """Validates faculty: must be non-empty and at most 100 characters."""
        return bool(faculty and faculty.strip()) and len(faculty.strip()) <= 100

    @staticmethod
    def validate_year_level(year_level) -> bool:
        """Validates year level: integer from 1 to 4."""
        try:
            value = int(year_level)
            return 1 <= value <= 4
        except (ValueError, TypeError):
            return False
