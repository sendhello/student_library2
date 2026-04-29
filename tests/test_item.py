from entities.item import Item


def test_item_init_stores_all_fields():
    item = Item(
        item_id=1,
        title="Clean Code",
        author="Robert C. Martin",
        faculty="Technology",
        year=2008,
        copies=3,
    )

    assert item.id == 1
    assert item.title == "Clean Code"
    assert item.author == "Robert C. Martin"
    assert item.faculty == "Technology"
    assert item.year == 2008
    assert item.copies == 3
    assert item.borrowed_by == []
    assert item.due_dates == {}


def test_item_is_available_when_new():
    item = Item(1, "Title", "Author", "Business", 2020, 2)
    assert item.is_available() is True


def test_item_is_available_false_when_all_copies_taken():
    item = Item(1, "Title", "Author", "Business", 2020, 1)
    item.borrow(1, "2026-05-06")
    assert item.is_available() is False


def test_item_borrow_increments_borrowers():
    item = Item(1, "Title", "Author", "Business", 2020, 2)

    result = item.borrow(1, "2026-05-06")

    assert result is True
    assert item.borrowed_by == [1]
    assert item.due_dates[1] == "2026-05-06"


def test_item_borrow_returns_false_when_no_copies():
    item = Item(1, "Title", "Author", "Business", 2020, 1)
    assert item.borrow(1, "2026-05-06") is True

    result = item.borrow(2, "2026-05-06")

    assert result is False
    assert item.borrowed_by == [1]
    assert 2 not in item.due_dates


def test_item_borrow_returns_false_when_same_member_twice():
    item = Item(1, "Title", "Author", "Business", 2020, 5)
    assert item.borrow(1, "2026-05-06") is True

    result = item.borrow(1, "2026-06-06")

    assert result is False
    assert item.borrowed_by == [1]
    assert item.due_dates[1] == "2026-05-06"


def test_item_return_removes_borrower():
    item = Item(1, "Title", "Author", "Business", 2020, 2)
    item.borrow(1, "2026-05-06")
    item.borrow(2, "2026-05-10")

    result = item.return_item(1)

    assert result is True
    assert 1 not in item.borrowed_by
    assert 1 not in item.due_dates
    assert item.borrowed_by == [2]
    assert item.due_dates[2] == "2026-05-10"


def test_item_return_returns_false_for_non_borrower():
    item = Item(1, "Title", "Author", "Business", 2020, 2)
    item.borrow(1, "2026-05-06")

    result = item.return_item(99)

    assert result is False
    assert item.borrowed_by == [1]
    assert item.due_dates[1] == "2026-05-06"


def test_item_available_copies_math():
    item = Item(1, "Title", "Author", "Business", 2020, 3)
    item.borrow(1, "2026-05-06")
    item.borrow(2, "2026-05-06")

    assert item.available_copies() == 1


def test_item_to_dict_roundtrip():
    item = Item(7, "Domain Driven Design", "Eric Evans", "Technology", 2003, 2)
    item.borrow(1, "2026-05-06")
    item.borrow(2, "2026-05-10")

    data = item.to_dict()
    restored = Item.from_dict(data)

    assert restored.id == item.id
    assert restored.title == item.title
    assert restored.author == item.author
    assert restored.faculty == item.faculty
    assert restored.year == item.year
    assert restored.copies == item.copies
    assert restored.borrowed_by == item.borrowed_by
    assert restored.due_dates == item.due_dates


def test_item_from_dict_defaults_empty_state():
    data = {
        "id": 5,
        "title": "Refactoring",
        "author": "Martin Fowler",
        "faculty": "Technology",
        "year": 1999,
        "copies": 1,
    }

    item = Item.from_dict(data)

    assert item.borrowed_by == []
    assert item.due_dates == {}
    assert item.is_available() is True
