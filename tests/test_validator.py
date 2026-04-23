from utils.validator import Validator


def test_validate_name():
    assert Validator.validate_name("John Doe") is True
    assert Validator.validate_name("") is False
    assert Validator.validate_name("   ") is False
    assert Validator.validate_name("A" * 50) is True
    assert Validator.validate_name("A" * 51) is False


def test_validate_non_empty():
    assert Validator.validate_non_empty("abc") is True
    assert Validator.validate_non_empty("   ") is False
    assert Validator.validate_non_empty("") is False


def test_validate_email():
    assert Validator.validate_email("test@email.com") is True
    assert Validator.validate_email("bademail") is False
    assert Validator.validate_email("test@.com") is False


def test_validate_phone():
    assert Validator.validate_phone("1234567") is True
    assert Validator.validate_phone("123456789012345") is True
    assert Validator.validate_phone("1234") is False
    assert Validator.validate_phone("abc123") is False


def test_validate_date():
    assert Validator.validate_date("2024-01-01") is True
    assert Validator.validate_date("01-01-2024") is False
    assert Validator.validate_date("2024/01/01") is False


def test_validate_faculty():
    assert Validator.validate_faculty("IT") is True
    assert Validator.validate_faculty("Business") is True
    assert Validator.validate_faculty("") is False
    assert Validator.validate_faculty("   ") is False


def test_validate_year_level():
    assert Validator.validate_year_level(1) is True
    assert Validator.validate_year_level(4) is True
    assert Validator.validate_year_level(0) is False
    assert Validator.validate_year_level(5) is False
    assert Validator.validate_year_level("abc") is False
