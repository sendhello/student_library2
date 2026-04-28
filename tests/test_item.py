import pytest
from entities.item import Item

def test_item_init_stores_all_fields():
    """Test that the Item constructor stores all 7 fields correctly."""
    item = Item(1, "Python Basics", "Guido van Rossum", "Engineering", 2020, 5)
    assert item.id == 1
    assert item.title == "Python Basics"
    assert item.author == "Guido van Rossum"
    assert item.faculty == "Engineering"
    assert item.year == 2020
    assert item.copies == 5
    assert item.borrowed_by == []
    assert item.due_dates == {}

def test_item_is_available_when_new():
    """Test that a new Item is available when no copies are borrowed."""
    item = Item(1, "Python Basics", "Guido van Rossum", "Engineering", 2020, 5)
    assert item.is_available() is True

def test_item_borrow_increments_borrowers():
    """Test that borrowing an item increments the borrowers list and sets the due date."""
    item = Item(1, "Python Basics", "Guido van Rossum", "Engineering", 2020, 5)
    assert item.borrow(1, "2026-05-06") is True
    assert item.borrowed_by == [1]
    assert item.due_dates[1] == "2026-05-06"

def test_item_borrow_returns_false_when_no_copies():
    """Test that borrowing an item returns False when no copies are available."""
    item = Item(1, "Python Basics", "Guido van Rossum", "Engineering", 2020, 1)
    assert item.borrow(1, "2026-05-06") is True
    assert item.borrow(2, "2026-05-06") is False

def test_item_borrow_returns_false_when_same_member_twice():
    """Test that borrowing an item returns False when the same member tries to borrow twice."""
    item = Item(1, "Python Basics", "Guido van Rossum", "Engineering", 2020, 5)
    assert item.borrow(1, "2026-05-06") is True
    assert item.borrow(1, "2026-05-06") is False
    assert item.borrowed_by == [1]
    assert item.due_dates[1] == "2026-05-06"

def test_item_return_removes_borrower():
    """Test that returning an item removes the borrower from the lists."""
    item = Item(1, "Python Basics", "Guido van Rossum", "Engineering", 2020, 5)
    item.borrow(1, "2026-05-06")
    assert item.return_item(1) is True
    assert item.borrowed_by == []
    assert item.due_dates == {}

def test_item_return_returns_false_for_non_borrower():
    """Test that returning an item returns False for a non-borrower."""
    item = Item(1, "Python Basics", "Guido van Rossum", "Engineering", 2020, 5)
    assert item.return_item(99) is False

def test_item_available_copies_math():
    """Test that available_copies returns the correct number of available copies."""
    item = Item(1, "Python Basics", "Guido van Rossum", "Engineering", 2020, 3)
    assert item.available_copies() == 3
    item.borrow(1, "2026-05-06")
    assert item.available_copies() == 2
    item.borrow(2, "2026-05-06")
    assert item.available_copies() == 1

def test_item_to_dict_roundtrip():
    """Test that to_dict and from_dict correctly round-trip the state."""
    item = Item(1, "Python Basics", "Guido van Rossum", "Engineering", 2020, 5)
    item.borrow(1, "2026-05-06")
    item.borrow(2, "2026-05-07")

    item_dict = item.to_dict()
    new_item = Item.from_dict(item_dict)

    assert new_item.id == item.id
    assert new_item.title == item.title
    assert new_item.author == item.author
    assert new_item.faculty == item.faculty
    assert new_item.year == item.year
    assert new_item.copies == item.copies
    assert new_item.borrowed_by == item.borrowed_by
    assert new_item.due_dates == item.due_dates

def test_item_to_dict_includes_all_fields():
    """Test that to_dict includes all fields."""
    item = Item(1, "Python Basics", "Guido van Rossum", "Engineering", 2020, 5)
    item.borrow(1, "2026-05-06")
    item_dict = item.to_dict()

    assert item_dict["id"] == 1
    assert item_dict["title"] == "Python Basics"
    assert item_dict["author"] == "Guido van Rossum"
    assert item_dict["faculty"] == "Engineering"
    assert item_dict["year"] == 2020
    assert item_dict["copies"] == 5
    assert item_dict["borrowed_by"] == [1]
    assert item_dict["due_dates"] == {1: "2026-05-06"}
