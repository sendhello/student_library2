import pytest
from library import Library
from datetime import date


@pytest.fixture
def empty_library(tmp_path):
    return Library()

@pytest.fixture
def seeded_library(tmp_path):
    library = Library()

    # Agregar 5 miembros
    library.add_member("Member 1", "member1@example.com", "1111111111", "2000-01-01", "Engineering", 1)
    library.add_member("Member 2", "member2@example.com", "2222222222", "2000-01-02", "Science", 2)
    library.add_member("Member 3", "member3@example.com", "3333333333", "2000-01-03", "Arts", 3)
    library.add_member("Member 4", "member4@example.com", "4444444444", "2000-01-04", "Business", 4)
    library.add_member("Member 5", "member5@example.com", "5555555555", "2000-01-05", "Law", 5)

    # Agregar 10 libros
    library.add_item("Book 1", "Author 1", "Engineering", 2000, 5)
    library.add_item("Book 2", "Author 2", "Science", 2001, 5)
    library.add_item("Book 3", "Author 3", "Arts", 2002, 5)
    library.add_item("Book 4", "Author 4", "Business", 2003, 5)
    library.add_item("Book 5", "Author 5", "Law", 2004, 5)
    library.add_item("Book 6", "Author 6", "Engineering", 2005, 5)
    library.add_item("Book 7", "Author 7", "Science", 2006, 5)
    library.add_item("Book 8", "Author 8", "Arts", 2007, 5)
    library.add_item("Book 9", "Author 9", "Business", 2008, 5)
    library.add_item("Book 10", "Author 10", "Law", 2009, 5)

    # Agregar 3 préstamos activos
    today = date.today().isoformat()
    library.borrow_item(1, 1, "2023-12-31")
    library.borrow_item(2, 2, "2023-12-31")
    library.borrow_item(3, 3, "2023-12-31")

    return library
