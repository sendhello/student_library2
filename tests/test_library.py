"""Tests for the Library class — TASK-06."""

import json
import os
import tempfile
import unittest

from library import Library


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


if __name__ == "__main__":
    unittest.main()
