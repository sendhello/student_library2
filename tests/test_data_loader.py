"""Unit tests for DataLoader."""
import os
import tempfile

import pytest

from data_loader import DataLoader
from exceptions import DataLoadError


def test_load_students():
    loader = DataLoader()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("student_id,name,email,phone,birthdate,faculty,year_level\n")
        f.write("1,Nate Bustamante,nate@example.com,1234567890,2000-01-01,Engineering,3\n")
        f.write("2,Alice Smith,alice@example.com,0987654321,1999-05-15,Science,2\n")
        temp_file = f.name

    members = loader.load_students(temp_file)
    assert len(members) == 2
    os.unlink(temp_file)


def test_load_books():
    loader = DataLoader()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("book_id,title,author,faculty,year,copies\n")
        f.write("1,Python Basics,Guido van Rossum,Engineering,2020,5\n")
        f.write("2,Clean Code,Robert C. Martin,Science,2008,3\n")
        temp_file = f.name

    items = loader.load_books(temp_file)
    assert len(items) == 2
    os.unlink(temp_file)


def test_load_history():
    loader = DataLoader()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("transaction_id,student_id,book_id,borrow_date,due_date,return_date\n")
        f.write("1,1,1,2023-01-01,2023-01-15,\n")
        f.write("2,2,2,2023-02-01,2023-02-15,2023-02-10\n")
        temp_file = f.name

    transactions = loader.load_history(temp_file)
    assert len(transactions) == 2
    # Empty return_date → None (active); filled → str (returned)
    assert transactions[0].return_date is None
    assert transactions[0].is_active() is True
    assert transactions[1].return_date == "2023-02-10"
    assert transactions[1].is_active() is False
    os.unlink(temp_file)


def test_missing_file():
    loader = DataLoader()
    with pytest.raises(DataLoadError):
        loader.load_students("nonexistent_file.csv")


def test_missing_column():
    loader = DataLoader()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("student_id,name,email,phone,birthdate\n")  # missing faculty, year_level
        f.write("1,Nate Bustamante,nate@example.com,1234567890,2000-01-01\n")
        temp_file = f.name

    with pytest.raises(DataLoadError):
        loader.load_students(temp_file)
    os.unlink(temp_file)


def test_malformed_row():
    loader = DataLoader()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("student_id,name,email,phone,birthdate,faculty,year_level\n")
        f.write("1,Nate Bustamante,nate@example.com,1234567890,2000-01-01,Engineering,3\n")
        f.write("2,Alice Smith,alice@example.com,0987654321,1999-05-15,Science,not_a_number\n")
        temp_file = f.name

    members = loader.load_students(temp_file)
    assert len(members) == 1  # malformed year_level row skipped
    os.unlink(temp_file)
