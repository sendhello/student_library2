"""Validator module for validating library data."""
class Validator:
    @staticmethod
    def validate_member_id(member_id):
        """Validate member ID"""
        return str(member_id).strip() != ""

    @staticmethod
    def validate_name(name):
        """Validate member name"""
        return str(name).strip() != ""

    @staticmethod
    def validate_email(email):
        """Validate email address"""
        email = str(email).strip()
        return "@" in email and "." in email and len(email) >= 5

    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        phone = str(phone).strip()
        return phone.isdigit() and len(phone) >= 8
