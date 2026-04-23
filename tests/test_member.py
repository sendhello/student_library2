from entities.member import Member


def test_member_init_stores_all_fields():
    member = Member(
        member_id=1,
        name="John Doe",
        email="john@email.com",
        phone="12345678",
        birthdate="2000-01-01",
        faculty="IT",
        year_level=2
    )

    assert member.id == 1
    assert member.name == "John Doe"
    assert member.email == "john@email.com"
    assert member.phone == "12345678"
    assert member.birthdate == "2000-01-01"
    assert member.faculty == "IT"
    assert member.year_level == 2


def test_member_to_dict_roundtrip():
    member = Member(
        1, "John Doe", "john@email.com",
        "12345678", "2000-01-01", "IT", 2
    )

    data = member.to_dict()
    restored = Member.from_dict(data)

    assert restored.id == member.id
    assert restored.name == member.name
    assert restored.faculty == member.faculty
    assert restored.year_level == member.year_level


def test_member_borrowed_items_default_empty():
    member = Member(
        1, "John Doe", "john@email.com",
        "12345678", "2000-01-01", "IT", 2
    )

    assert member.get_borrowed_items() == []


def test_member_borrowed_items_append_and_remove():
    member = Member(
        1, "John Doe", "john@email.com",
        "12345678", "2000-01-01", "IT", 2
    )

    member.borrow_item(10)
    assert 10 in member.get_borrowed_items()

    member.return_item(10)
    assert 10 not in member.get_borrowed_items()
