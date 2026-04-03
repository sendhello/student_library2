"""Tests for the Library class and entity classes."""

import json
import os
import tempfile
import unittest

from library import Library
from entities.item import Item
from entities.member import Member
from entities.base import BaseEntity


class TestLibraryInit(unittest.TestCase):
    """Tests for __init__ signature."""

    def test_init_no_args_uses_default_data_file(self):
        """Library() with no arguments must default data_file to 'data.json'."""
        lib = Library()
        self.assertEqual(lib.data_file, "data.json")

    def test_init_custom_data_file(self):
        """Library(data_file=...) must store the given path."""
        lib = Library(data_file="test_data.json")
        self.assertEqual(lib.data_file, "test_data.json")

    def test_init_members_and_items_are_empty_lists(self):
        """Fresh Library must have empty members and items lists."""
        lib = Library()
        self.assertEqual(lib.members, [])
        self.assertEqual(lib.items, [])


class TestAddMember(unittest.TestCase):
    """Tests for add_member — must accept birthdate."""

    def setUp(self):
        self.lib = Library()

    def test_add_member_returns_member_with_correct_fields(self):
        """add_member must accept birthdate and return a Member with all fields set."""
        member = self.lib.add_member("Alice Smith", "alice@example.com", "0412345678", "1995-04-12")
        self.assertEqual(member.name, "Alice Smith")
        self.assertEqual(member.email, "alice@example.com")
        self.assertEqual(member.phone, "0412345678")
        self.assertEqual(member.birthdate, "1995-04-12")

    def test_add_member_assigns_sequential_id(self):
        """Each added member must receive an incrementing integer ID."""
        m1 = self.lib.add_member("Alice", "a@b.com", "0400000001", "1990-01-01")
        m2 = self.lib.add_member("Bob", "b@b.com", "0400000002", "1991-02-02")
        self.assertEqual(m1.id, 1)
        self.assertEqual(m2.id, 2)


class TestFindMember(unittest.TestCase):
    """Tests for find_member — must use member.id, not member.member_id."""

    def setUp(self):
        self.lib = Library()
        self.lib.add_member("Alice", "a@b.com", "0400000001", "1990-01-01")

    def test_find_existing_member_returns_member(self):
        """find_member(1) must return the Member with id 1."""
        member = self.lib.find_member(1)
        self.assertIsNotNone(member)
        self.assertEqual(member.id, 1)

    def test_find_nonexistent_member_returns_none(self):
        """find_member with unknown ID must return None."""
        self.assertIsNone(self.lib.find_member(999))


class TestRemoveMember(unittest.TestCase):
    """Tests for remove_member."""

    def setUp(self):
        self.lib = Library()
        self.lib.add_member("Alice", "a@b.com", "0400000001", "1990-01-01")
        self.lib.add_member("Bob", "b@b.com", "0400000002", "1991-02-02")

    def test_remove_existing_member_returns_true(self):
        """remove_member with a valid ID must return True and shrink the list."""
        result = self.lib.remove_member(1)
        self.assertTrue(result)
        self.assertEqual(len(self.lib.members), 1)

    def test_remove_existing_member_is_no_longer_findable(self):
        """After removal, find_member must return None for that ID."""
        self.lib.remove_member(1)
        self.assertIsNone(self.lib.find_member(1))

    def test_remove_nonexistent_member_returns_false(self):
        """remove_member with an unknown ID must return False."""
        result = self.lib.remove_member(999)
        self.assertFalse(result)

    def test_remove_member_does_not_affect_others(self):
        """Removing member 1 must not remove member 2."""
        self.lib.remove_member(1)
        self.assertIsNotNone(self.lib.find_member(2))

    def test_remove_member_clears_borrowed_by_on_items(self):
        """Removing a member must clear borrowed_by on any items they had borrowed."""
        item = self.lib.add_item("Clean Code", "Robert Martin")
        self.lib.borrow_item(1, item.id, "2026-05-01")
        self.lib.remove_member(1)
        self.assertIsNone(item.borrowed_by)
        self.assertIsNone(item.due_date)


class TestAddItem(unittest.TestCase):
    """Tests for add_item."""

    def setUp(self):
        self.lib = Library()

    def test_add_item_returns_item_with_correct_fields(self):
        """add_item must return an Item with correct title and author."""
        item = self.lib.add_item("Clean Code", "Robert Martin")
        self.assertEqual(item.title, "Clean Code")
        self.assertEqual(item.author, "Robert Martin")

    def test_add_item_assigns_sequential_id(self):
        """Each added item must receive an incrementing integer ID."""
        i1 = self.lib.add_item("Clean Code", "Robert Martin")
        i2 = self.lib.add_item("The Pragmatic Programmer", "Hunt & Thomas")
        self.assertEqual(i1.id, 1)
        self.assertEqual(i2.id, 2)

    def test_add_item_is_available_by_default(self):
        """Newly added item must be available (not borrowed)."""
        item = self.lib.add_item("Clean Code", "Robert Martin")
        self.assertTrue(item.is_available())


class TestBorrowReturnItem(unittest.TestCase):
    """Tests for borrow_item and return_item."""

    def setUp(self):
        self.lib = Library()
        self.member = self.lib.add_member("Alice", "a@b.com", "0400000001", "1990-01-01")
        self.item = self.lib.add_item("Clean Code", "Robert Martin")

    def test_borrow_item_returns_true(self):
        """borrow_item must return True on success."""
        result = self.lib.borrow_item(self.member.id, self.item.id, "2026-05-01")
        self.assertTrue(result)

    def test_borrow_item_marks_item_unavailable(self):
        """After borrowing, item must not be available."""
        self.lib.borrow_item(self.member.id, self.item.id, "2026-05-01")
        self.assertFalse(self.item.is_available())

    def test_borrow_item_adds_to_member_borrowed_items(self):
        """After borrowing, item ID must appear in member's borrowed_items."""
        self.lib.borrow_item(self.member.id, self.item.id, "2026-05-01")
        self.assertIn(self.item.id, self.member.borrowed_items)

    def test_borrow_already_borrowed_item_returns_false(self):
        """Borrowing an already-borrowed item must return False."""
        self.lib.borrow_item(self.member.id, self.item.id, "2026-05-01")
        result = self.lib.borrow_item(self.member.id, self.item.id, "2026-06-01")
        self.assertFalse(result)

    def test_borrow_nonexistent_member_returns_false(self):
        """borrow_item with unknown member ID must return False."""
        self.assertFalse(self.lib.borrow_item(999, self.item.id, "2026-05-01"))

    def test_borrow_nonexistent_item_returns_false(self):
        """borrow_item with unknown item ID must return False."""
        self.assertFalse(self.lib.borrow_item(self.member.id, 999, "2026-05-01"))

    def test_return_item_returns_true(self):
        """return_item must return True when item is successfully returned."""
        self.lib.borrow_item(self.member.id, self.item.id, "2026-05-01")
        result = self.lib.return_item(self.member.id, self.item.id)
        self.assertTrue(result)

    def test_return_item_makes_item_available_again(self):
        """After returning, item must be available again."""
        self.lib.borrow_item(self.member.id, self.item.id, "2026-05-01")
        self.lib.return_item(self.member.id, self.item.id)
        self.assertTrue(self.item.is_available())

    def test_return_item_removes_from_member_borrowed_items(self):
        """After returning, item ID must be removed from member's borrowed_items."""
        self.lib.borrow_item(self.member.id, self.item.id, "2026-05-01")
        self.lib.return_item(self.member.id, self.item.id)
        self.assertNotIn(self.item.id, self.member.borrowed_items)

    def test_return_item_not_borrowed_by_member_returns_false(self):
        """return_item when member didn't borrow the item must return False."""
        result = self.lib.return_item(self.member.id, self.item.id)
        self.assertFalse(result)


class TestJsonPersistence(unittest.TestCase):
    """Tests for save_to_json and load_from_json."""

    def setUp(self):
        """Each test gets its own temporary JSON file."""
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w")
        self.tmp.write('{"members": [], "items": []}')
        self.tmp.close()
        self.lib = Library(data_file=self.tmp.name)

    def tearDown(self):
        """Delete the temp file after each test."""
        if os.path.exists(self.tmp.name):
            os.remove(self.tmp.name)

    def test_save_creates_valid_json_file(self):
        """save_to_json must write a file that is valid JSON."""
        self.lib.save_to_json()
        with open(self.tmp.name) as f:
            data = json.load(f)
        self.assertIn("members", data)
        self.assertIn("items", data)

    def test_save_persists_members(self):
        """save_to_json must serialise all members to the file."""
        self.lib.add_member("Alice", "a@b.com", "0412345678", "1995-04-12")
        self.lib.save_to_json()
        with open(self.tmp.name) as f:
            data = json.load(f)
        self.assertEqual(len(data["members"]), 1)
        self.assertEqual(data["members"][0]["name"], "Alice")
        self.assertEqual(data["members"][0]["birthdate"], "1995-04-12")

    def test_save_persists_items(self):
        """save_to_json must serialise all items to the file."""
        self.lib.add_item("Clean Code", "Robert Martin")
        self.lib.save_to_json()
        with open(self.tmp.name) as f:
            data = json.load(f)
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["title"], "Clean Code")

    def test_save_persists_borrow_state(self):
        """save_to_json must preserve borrowed_by and due_date on items."""
        m = self.lib.add_member("Alice", "a@b.com", "0412345678", "1995-04-12")
        item = self.lib.add_item("Clean Code", "Robert Martin")
        self.lib.borrow_item(m.id, item.id, "2026-05-01")
        self.lib.save_to_json()
        with open(self.tmp.name) as f:
            data = json.load(f)
        self.assertEqual(data["items"][0]["borrowed_by"], m.id)
        self.assertEqual(data["items"][0]["due_date"], "2026-05-01")
        self.assertIn(item.id, data["members"][0]["borrowed_items"])

    def test_load_restores_members(self):
        """load_from_json must rebuild the members list from the file."""
        self.lib.add_member("Alice", "a@b.com", "0412345678", "1995-04-12")
        self.lib.save_to_json()
        lib2 = Library(data_file=self.tmp.name)
        lib2.load_from_json()
        self.assertEqual(len(lib2.members), 1)
        self.assertEqual(lib2.members[0].name, "Alice")
        self.assertEqual(lib2.members[0].birthdate, "1995-04-12")

    def test_load_restores_items(self):
        """load_from_json must rebuild the items list from the file."""
        self.lib.add_item("Clean Code", "Robert Martin")
        self.lib.save_to_json()
        lib2 = Library(data_file=self.tmp.name)
        lib2.load_from_json()
        self.assertEqual(len(lib2.items), 1)
        self.assertEqual(lib2.items[0].title, "Clean Code")

    def test_load_restores_borrow_state(self):
        """load_from_json must restore borrowed_by/due_date and borrowed_items."""
        m = self.lib.add_member("Alice", "a@b.com", "0412345678", "1995-04-12")
        item = self.lib.add_item("Clean Code", "Robert Martin")
        self.lib.borrow_item(m.id, item.id, "2026-05-01")
        self.lib.save_to_json()
        lib2 = Library(data_file=self.tmp.name)
        lib2.load_from_json()
        self.assertEqual(lib2.items[0].borrowed_by, m.id)
        self.assertIn(item.id, lib2.members[0].borrowed_items)

    def test_load_on_missing_file_leaves_lists_empty(self):
        """load_from_json must not crash when the file does not exist."""
        lib = Library(data_file="nonexistent_99999.json")
        lib.load_from_json()
        self.assertEqual(lib.members, [])
        self.assertEqual(lib.items, [])

    def test_load_on_empty_file_leaves_lists_empty(self):
        """load_from_json on a file with empty JSON object must not crash."""
        with open(self.tmp.name, "w") as f:
            f.write("{}")
        lib = Library(data_file=self.tmp.name)
        lib.load_from_json()
        self.assertEqual(lib.members, [])
        self.assertEqual(lib.items, [])


class TestItemBaseEntity(unittest.TestCase):
    """Tests confirming Item properly inherits BaseEntity."""

    def test_item_is_instance_of_base_entity(self):
        """Item must be a subclass of BaseEntity."""
        item = Item(1, "Clean Code", "Robert Martin")
        self.assertIsInstance(item, BaseEntity)

    def test_item_id_via_property(self):
        """Item.id must return the value passed to the constructor."""
        item = Item(42, "Clean Code", "Robert Martin")
        self.assertEqual(item.id, 42)

    def test_item_id_is_read_only(self):
        """Assigning to item.id must raise AttributeError."""
        item = Item(1, "Clean Code", "Robert Martin")
        with self.assertRaises(AttributeError):
            setattr(item, "id", 99)

    def test_item_equality_by_id(self):
        """Two Items with the same ID must be equal regardless of title."""
        item_a = Item(5, "Title A", "Author A")
        item_b = Item(5, "Title B", "Author B")
        self.assertEqual(item_a, item_b)

    def test_item_inequality_different_id(self):
        """Two Items with different IDs must not be equal."""
        self.assertNotEqual(Item(1, "A", "A"), Item(2, "A", "A"))

    def test_item_from_dict_is_classmethod(self):
        """from_dict must be a classmethod and return an Item instance."""
        data = {"id": 3, "title": "Refactoring", "author": "Fowler",
                "borrowed_by": None, "due_date": None}
        item = Item.from_dict(data)
        self.assertIsInstance(item, Item)
        self.assertEqual(item.id, 3)
        self.assertEqual(item.title, "Refactoring")


class TestMemberEntity(unittest.TestCase):
    """Tests for Member class behaviour."""

    def test_member_is_instance_of_base_entity(self):
        """Member must be a subclass of BaseEntity."""
        m = Member(1, "Alice", "a@b.com", "0400000001", "1990-01-01")
        self.assertIsInstance(m, BaseEntity)

    def test_member_borrow_item_adds_id(self):
        """borrow_item must add the item ID to borrowed_items."""
        m = Member(1, "Alice", "a@b.com", "0400000001", "1990-01-01")
        m.borrow_item(7)
        self.assertIn(7, m.borrowed_items)

    def test_member_borrow_item_no_duplicates(self):
        """Calling borrow_item twice with same ID must not add a duplicate."""
        m = Member(1, "Alice", "a@b.com", "0400000001", "1990-01-01")
        m.borrow_item(7)
        m.borrow_item(7)
        self.assertEqual(m.borrowed_items.count(7), 1)

    def test_member_return_item_removes_id(self):
        """return_item must remove the item ID from borrowed_items."""
        m = Member(1, "Alice", "a@b.com", "0400000001", "1990-01-01")
        m.borrow_item(7)
        m.return_item(7)
        self.assertNotIn(7, m.borrowed_items)

    def test_member_get_borrowed_items(self):
        """get_borrowed_items must return the current list of borrowed IDs."""
        m = Member(1, "Alice", "a@b.com", "0400000001", "1990-01-01")
        m.borrow_item(3)
        m.borrow_item(5)
        self.assertEqual(m.get_borrowed_items(), [3, 5])

    def test_member_from_dict_round_trip(self):
        """to_dict → from_dict must produce an equivalent Member."""
        m = Member(1, "Alice", "alice@example.com", "0412345678", "1990-01-01")
        m.borrow_item(2)
        restored = Member.from_dict(m.to_dict())
        self.assertEqual(restored.id, m.id)
        self.assertEqual(restored.email, m.email)
        self.assertEqual(restored.phone, m.phone)
        self.assertEqual(restored.birthdate, m.birthdate)
        self.assertEqual(restored.borrowed_items, m.borrowed_items)


class TestGetAvailableAndFindItem(unittest.TestCase):
    """Tests for Library.get_available_items and find_item."""

    def setUp(self):
        self.lib = Library()
        self.member = self.lib.add_member("Alice", "a@b.com", "0400000001", "1990-01-01")
        self.item1 = self.lib.add_item("Clean Code", "Martin")
        self.item2 = self.lib.add_item("Refactoring", "Fowler")
        self.lib.borrow_item(self.member.id, self.item1.id, "2026-05-01")

    def test_get_available_items_excludes_borrowed(self):
        """get_available_items must not include borrowed items."""
        available = self.lib.get_available_items()
        self.assertNotIn(self.item1, available)

    def test_get_available_items_includes_free(self):
        """get_available_items must include non-borrowed items."""
        available = self.lib.get_available_items()
        self.assertIn(self.item2, available)

    def test_find_item_returns_correct_item(self):
        """find_item must return the item matching the given ID."""
        found = self.lib.find_item(self.item2.id)
        self.assertEqual(found, self.item2)

    def test_find_item_returns_none_for_unknown_id(self):
        """find_item with unknown ID must return None."""
        self.assertIsNone(self.lib.find_item(999))


if __name__ == "__main__":
    unittest.main()
