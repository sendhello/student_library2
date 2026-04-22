import pytest

from entities.transaction import Transaction


# ---------- is_active ----------

def test_transaction_is_active_when_return_date_none():
    """A transaction with return_date=None represents an active loan."""

    t = Transaction(1, 10, 100, "2026-04-01", "2026-04-15")
    assert t.is_active() is True


def test_transaction_is_active_false_when_returned():
    """A transaction with any return_date string is no longer active."""

    t = Transaction(1, 10, 100, "2026-04-01", "2026-04-15", return_date="2026-04-10")
    assert t.is_active() is False


# ---------- is_overdue for returned loans ----------

def test_transaction_is_overdue_true_when_returned_late():
    """Returned after due_date → overdue, regardless of `today`."""

    t = Transaction(1, 10, 100, "2026-04-01", "2026-04-15", return_date="2026-04-20")
    assert t.is_overdue("2026-05-01") is True
    # `today` must be ignored for returned loans
    assert t.is_overdue("2026-04-15") is True


def test_transaction_is_overdue_false_when_returned_on_time():
    """Returned on or before due_date → not overdue."""

    on_time = Transaction(1, 10, 100, "2026-04-01", "2026-04-15", return_date="2026-04-15")
    early = Transaction(2, 10, 100, "2026-04-01", "2026-04-15", return_date="2026-04-10")
    assert on_time.is_overdue("2099-01-01") is False
    assert early.is_overdue("2099-01-01") is False


# ---------- is_overdue for active loans ----------

def test_transaction_is_overdue_uses_today_when_active():
    """Active loan: overdue iff `today` is past `due_date`."""

    t = Transaction(1, 10, 100, "2026-04-01", "2026-04-15")
    assert t.is_overdue("2026-04-20") is True     # today past due
    assert t.is_overdue("2026-04-10") is False    # today before due
    assert t.is_overdue("2026-04-15") is False    # today == due, not strictly past


# ---------- to_dict / from_dict round-trip ----------

def test_transaction_to_dict_roundtrip_active():
    """Active loan (return_date=None) survives serialisation."""

    original = Transaction(42, 10, 100, "2026-04-01", "2026-04-15")
    data = original.to_dict()

    assert data == {
        "id": 42,
        "member_id": 10,
        "item_id": 100,
        "borrow_date": "2026-04-01",
        "due_date": "2026-04-15",
        "return_date": None,
    }

    restored = Transaction.from_dict(data)
    assert restored.id == original.id
    assert restored.member_id == original.member_id
    assert restored.item_id == original.item_id
    assert restored.borrow_date == original.borrow_date
    assert restored.due_date == original.due_date
    assert restored.return_date is None
    assert restored.is_active() is True


def test_transaction_to_dict_roundtrip_returned():
    """Returned loan round-trips with a non-null return_date."""

    original = Transaction(7, 10, 100, "2026-04-01", "2026-04-15", return_date="2026-04-20")
    restored = Transaction.from_dict(original.to_dict())

    assert restored.id == 7
    assert restored.return_date == "2026-04-20"
    assert restored.is_active() is False
    assert restored.is_overdue("2026-05-01") is True


# ---------- extras beyond the minimum spec ----------

def test_transaction_equality_follows_base_entity_semantics():
    """BaseEntity equality: same type + same id, regardless of other fields."""

    a = Transaction(1, 10, 100, "2026-04-01", "2026-04-15")
    b = Transaction(1, 99, 999, "2099-01-01", "2099-01-15", return_date="2099-02-01")
    c = Transaction(2, 10, 100, "2026-04-01", "2026-04-15")
    assert a == b
    assert a != c


def test_transaction_id_is_read_only():
    """`id` is exposed via a read-only BaseEntity property."""

    t = Transaction(1, 10, 100, "2026-04-01", "2026-04-15")
    with pytest.raises(AttributeError):
        t.id = 2  # type: ignore[misc]
