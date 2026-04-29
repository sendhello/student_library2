import pytest
from library import Library, NotFoundError, BorrowingError
from datetime import date


def test_add_member(empty_library):
    member = empty_library.add_member("Nate Bustamante", "nate@example.com", "1234567890", "2000-01-01", "Engineering", 3)
    assert len(empty_library.members) == 1
    assert member.name == "Nate Bustamante"

def test_add_item(empty_library):
    item = empty_library.add_item("Python Basics", "Guido van Rossum", "Engineering", 2020, 5)
    assert len(empty_library.items) == 1
    assert item.title == "Python Basics"

def test_next_member_id_regression(empty_library):
    empty_library.add_member("Member 1", "m1@example.com", "111", "2000-01-01", "Science", 1)
    empty_library.add_member("Member 2", "m2@example.com", "222", "2000-01-01", "Science", 1)
    empty_library.add_member("Member 3", "m3@example.com", "333", "2000-01-01", "Science", 1)
    empty_library.members = [m for m in empty_library.members if m.id != 2]
    new_member = empty_library.add_member("Member 4", "m4@example.com", "444", "2000-01-01", "Science", 1)
    assert new_member.id == 4

def test_borrow_happy_path(seeded_library):
    transaction = seeded_library.borrow_item(4, 4, "2023-12-31")
    assert len(seeded_library.transactions) == 4
    assert transaction.is_active()
    assert 4 in seeded_library.find_member(4).get_borrowed_items()
    assert 4 in seeded_library.find_item(4).borrowed_by
    assert seeded_library.find_item(4).due_dates[4] == "2023-12-31"

def test_borrow_unknown_member(empty_library):
    with pytest.raises(NotFoundError):
        empty_library.borrow_item(999, 1, "2023-12-31")

def test_borrow_no_copies(seeded_library):
    # Exhaust all 5 copies of item 5 with 5 different members
    for member_id in range(1, 6):
        seeded_library.borrow_item(member_id, 5, "2023-12-31")
    # A 6th borrower can't get a copy — supply is exhausted
    sixth = seeded_library.add_member(
        "Member 6", "m6@example.com", "666", "2000-01-06", "Engineering", 1,
    )
    with pytest.raises(BorrowingError):
        seeded_library.borrow_item(sixth.id, 5, "2023-12-31")

def test_borrow_same_member_twice(seeded_library):
    with pytest.raises(BorrowingError):
        seeded_library.borrow_item(1, 1, "2023-12-31")

def test_return_happy_path(seeded_library):
    transaction = seeded_library.return_item(1, 1)
    assert not transaction.is_active()
    assert 1 not in seeded_library.find_member(1).get_borrowed_items()
    assert 1 not in seeded_library.find_item(1).borrowed_by
    assert 1 not in seeded_library.find_item(1).due_dates

def test_return_no_active_loan(seeded_library):
    with pytest.raises(BorrowingError):
        seeded_library.return_item(4, 4)

def test_remove_member_cascade(seeded_library):
    assert seeded_library.remove_member(1)
    assert len(seeded_library.members) == 4
    # Member 1's transactions are not deleted, just closed (return_date set)
    member_1_txns = [txn for txn in seeded_library.transactions if txn.member_id == 1]
    assert member_1_txns, "expected member 1's transaction history to remain"
    assert all(not txn.is_active() for txn in member_1_txns)
    # Item 1's copy is freed back to the pool
    assert 1 not in seeded_library.find_item(1).borrowed_by
    assert 1 not in seeded_library.find_item(1).due_dates

def test_save_and_load_json(empty_library, tmp_path):
    file_path = str(tmp_path / "data.json")
    empty_library.save_to_json(file_path)
    new_library = Library()
    new_library.load_from_json(file_path)
    assert new_library.is_empty()

def test_is_empty(empty_library, seeded_library):
    assert empty_library.is_empty()
    assert not seeded_library.is_empty()

def test_filter_transactions(seeded_library):
    active_txns = seeded_library.filter_transactions(status="active")
    assert len(active_txns) == 3
    member_txns = seeded_library.filter_transactions(member_id=1)
    assert len(member_txns) == 1
    item_txns = seeded_library.filter_transactions(item_id=1)
    assert len(item_txns) == 1
