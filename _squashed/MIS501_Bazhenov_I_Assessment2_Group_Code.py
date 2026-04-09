"""
MIS501 — Assessment 2 (Group)
Library Membership & Resource Management System

Team:
  Ivan Bazhenov    — TL (architect, reviewer, integration, main entry point)
  Takunda Audrey Shelter — D1 (Member class, Validator, Members UI, Flowchart)
  Renato Bustamante      — D2 (Item class, Display, Library part 2, Items UI)

This file is the combined single-file submission of a multi-module application.
The original project is structured across the following modules (boundaries are
marked with section banners below):

  entities/base.py      — BaseEntity abstract base class
  entities/member.py    — Member class
  entities/item.py      — Item class
  utils/validator.py    — Validator utility class
  utils/display.py      — Display utility class
  library.py            — Library data manager
  main.py               — Entry point and menu flows
"""

# ==============================================================================
# STDLIB IMPORTS
# (collected from all modules into a single block)
# ==============================================================================

import json
import os
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Self


# ==============================================================================
# MODULE: entities/base.py
# BaseEntity — Abstract base class for library entities
# Author: Ivan Bazhenov
# ==============================================================================

class BaseEntity(ABC):
    """
    Abstract base class for library entities.

    Subclasses must implement to_dict() and from_dict().
    """

    def __init__(self, _id: int):
        self._id = _id

    @property
    def id(self) -> int:
        """Read-only entity ID."""

        return self._id

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialise the entity to a plain dictionary for JSON storage."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> Self:
        """Deserialise an entity from a dictionary (loaded from JSON)."""
        ...

    def __eq__(self, other: object) -> bool:
        """Two entities are equal if they share the same type and ID."""

        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._id == other._id

    def __hash__(self) -> int:
        """Allow entities to be used in sets and as dict keys."""

        return hash((self.__class__.__name__, self._id))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id})"


# ==============================================================================
# MODULE: entities/member.py
# Member — Represents a library member
# Author: Takunda Audrey Shelter
# ==============================================================================

# from entities.base import BaseEntity  # (combined into single file)


class Member(BaseEntity):
    """
    Represents a library member.
    Stores personal details and borrowed items.
    """

    def __init__(self, member_id: int, name: str, email: str, phone: str, birthdate: str):
        super().__init__(member_id)
        self.name = name
        self.birthdate = birthdate
        self.email = email
        self.phone = phone
        self.borrowed_items = []

    def borrow_item(self, item_id: int) -> None:
        """Adds an item ID to the member's borrowed items list."""
        if item_id not in self.borrowed_items:
            self.borrowed_items.append(item_id)

    def return_item(self, item_id: int) -> None:
        """Removes an item ID from the member's borrowed items list."""
        if item_id in self.borrowed_items:
            self.borrowed_items.remove(item_id)

    def get_borrowed_items(self) -> list:
        """Returns the list of borrowed item IDs."""
        return self.borrowed_items

    def to_dict(self) -> dict:
        """Converts the instance into a dictionary for JSON storage."""
        return {
            "id": self.id,
            "name": self.name,
            "birthdate": self.birthdate,
            "email": self.email,
            "phone": self.phone,
            "borrowed_items": self.borrowed_items
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Member object from a dictionary."""
        member = cls(
            member_id=data["id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            birthdate=data["birthdate"]
        )
        member.borrowed_items = data.get("borrowed_items", [])
        return member

    def __str__(self) -> str:
        """Returns a human-readable string representation."""
        return (
            f"Member ID: {self.id} | Name: {self.name} | Email: {self.email} "
            f"| Phone: {self.phone} | Birthdate: {self.birthdate}"
        )

    def __repr__(self) -> str:
        return self.__str__()


# ==============================================================================
# MODULE: entities/item.py
# Item — Represents a library resource
# Author: Renato Bustamante
# ==============================================================================

# from entities.base import BaseEntity  # (combined into single file)


class Item(BaseEntity):
    """
    Represents a library resource.
    Handles the borrowing status and conversion to dictionaries for persistence.
    """

    def __init__(self, item_id: int, title: str, author: str):
        """Initializes an item with an ID, title, and author."""
        super().__init__(item_id)
        self.title = title
        self.author = author
        self.borrowed_by = None  # Stores the member's ID (int)
        self.due_date = None     # Format 'YYYY-MM-DD' (str)

    def borrow(self, member_id: int, due_date: str) -> bool:
        """Assigns the item to a member and sets the due date."""
        if self.is_available():
            self.borrowed_by = member_id
            self.due_date = due_date
            return True
        return False

    def return_item(self) -> bool:
        """Resets the item's status to available."""
        if not self.is_available():
            self.borrowed_by = None
            self.due_date = None
            return True
        return False

    def is_available(self) -> bool:
        """Checks if the item is currently not borrowed."""
        return self.borrowed_by is None

    def to_dict(self) -> dict:
        """Converts the instance into a dictionary for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "borrowed_by": self.borrowed_by,
            "due_date": self.due_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        """Creates an Item object from a data dictionary."""
        item = cls(data['id'], data['title'], data['author'])
        item.borrowed_by = data.get('borrowed_by')
        item.due_date = data.get('due_date')
        return item

    def __str__(self) -> str:
        """Returns a human-readable string representation."""
        return f"Item ID: {self.id} | Title: {self.title} | Author: {self.author}"


# ==============================================================================
# MODULE: utils/validator.py
# Validator — Static validation methods
# Author: Takunda Audrey Shelter
# ==============================================================================

# from datetime import datetime  # (combined into single file)
# import re                       # (combined into single file)


class Validator:
    """Provides static validation methods."""

    @staticmethod
    def validate_name(name: str) -> bool:
        """Validates member name: non-empty, max 50 characters."""
        return bool(name and name.strip()) and len(name.strip()) <= 50

    @staticmethod
    def validate_non_empty(value: str) -> bool:
        """Checks that a string is not empty."""
        return bool(value and value.strip())

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validates basic email format."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validates phone number (digits only, 7–15 chars)."""
        return phone.isdigit() and 7 <= len(phone) <= 15

    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Validates date format (YYYY-MM-DD)."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False


# ==============================================================================
# MODULE: utils/display.py
# Display — Static console output methods
# Author: Renato Bustamante
# ==============================================================================

class Display:
    """Static class for the console user interface."""

    @staticmethod
    def print_header(title: str) -> None:
        """Prints a decorated title bar."""
        print("\n" + "-" * 70)
        print(f"{title.upper():^70}")
        print("-" * 70)

    @staticmethod
    def print_menu(title: str, options: list[str]) -> None:
        """Prints a numbered menu based on a list of options."""
        Display.print_header(title)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("0. Back")

    @staticmethod
    def print_members_table(members: list) -> None:
        """Displays the members table using the original format from library.py."""
        print(f"| {'Member ID':10} | {'Name':20} | {'Email':30} | {'Phone':15} | {'Birthdate':12} |")
        print("-" * 100)
        for m in members:
            mid = m.id if hasattr(m, 'id') else m['id']
            name = m.name if hasattr(m, 'name') else m['name']
            email = m.email if hasattr(m, 'email') else m['email']
            phone = m.phone if hasattr(m, 'phone') else m['phone']
            bd = m.birthdate if hasattr(m, 'birthdate') else m['birthdate']
            print(f"| {mid:10} | {name:20} | {email:30} | {phone:15} | {bd:12} |")
        print("-" * 100)

    @staticmethod
    def print_items_table(items: list) -> None:
        """Displays the items table with availability status."""
        print(f"| {'Item ID':10} | {'Title':38} | {'Author':30} | {'Status':10} |")
        print("-" * 100)
        for item in items:
            status = "Borrowed" if not item.is_available() else "Available"
            print(f"| {item.id:10} | {item.title:38} | {item.author:30} | {status:10} |")
        print("-" * 100)

    @staticmethod
    def print_grouped_by_date(grouped: dict) -> None:
        """Prints items grouped by their due date."""
        for date, items in grouped.items():
            print(f"\nDue Date: {date}")
            print(f"| {'Item ID':10} | {'Title':40} | {'Author':30} |")
            print("-" * 90)
            for item in items:
                print(f"| {item.id:10} | {item.title:40} | {item.author:30} |")
            print("-" * 90)

    @staticmethod
    def print_success(msg: str) -> None:
        """Displays a success message."""
        print(f"\n>>> SUCCESS: {msg}")

    @staticmethod
    def print_error(msg: str) -> None:
        """Displays an error message."""
        print(f"\n!!! ERROR: {msg}")


# ==============================================================================
# MODULE: library.py
# Library — Central data manager
# Author: Renato Bustamante
# ==============================================================================

# import json                          # (combined into single file)
# import os                            # (combined into single file)
# from entities.item import Item       # (combined into single file)
# from entities.member import Member   # (combined into single file)


class Library:
    def __init__(self, data_file: str = "data.json"):
        """Initialises the Library with empty member and item lists."""

        self.data_file = data_file
        self.members: list = []
        self.items: list = []

    # -----------------------------
    # ITEM MANAGEMENT
    # -----------------------------
    def add_item(self, title: str, author: str) -> Item:
        """Creates, adds, and returns a new Item instance."""

        new_id = len(self.items) + 1
        new_item = Item(new_id, title.strip().title(), author.strip().title())
        self.items.append(new_item)
        return new_item

    def find_item(self, item_id: int):
        """Searches for an item by ID. Returns None if it does not exist."""

        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def get_all_items(self) -> list:
        """Returns the complete list of items."""

        return self.items

    def get_available_items(self) -> list:
        """Returns only the items that are currently not borrowed."""

        return [item for item in self.items if item.is_available()]

    # -----------------------------
    # MEMBER MANAGEMENT
    # -----------------------------
    def add_member(self, name: str, email: str, phone: str, birthdate: str) -> "Member":
        """Creates, adds, and returns a new Member instance."""

        new_id = len(self.members) + 1
        new_member = Member(
            new_id,
            name.strip().title(),
            email.strip(),
            phone.strip(),
            birthdate.strip(),
        )
        self.members.append(new_member)
        return new_member

    def find_member(self, member_id: int):
        """Searches for a member by their unique ID."""

        for member in self.members:
            if member.id == member_id:
                return member
        return None

    def get_all_members(self) -> list:
        """Returns the complete list of members."""

        return self.members

    def remove_member(self, member_id: int) -> bool:
        """Removes a member from the library by their unique ID."""

        member = self.find_member(member_id)
        if member is None:
            return False
        self.members.remove(member)
        for item in self.items:
            if item.borrowed_by == member_id:
                item.borrowed_by = None
                item.due_date = None
        return True

    # -----------------------------
    # BORROWING / RETURN MANAGEMENT
    # -----------------------------
    def borrow_item(self, member_id: int, item_id: int, due_date: str) -> bool:
        """
        Manages the borrowing process by validating edge cases.
        Updates both the Item object and the Member's list.
        """
        member = self.find_member(member_id)
        item = self.find_item(item_id)

        if not member:
            return False
        if not item:
            return False
        if not item.is_available():
            return False

        if item.borrow(member_id, due_date):
            member.borrowed_items.append(item_id)
            return True
        return False

    def return_item(self, member_id: int, item_id: int) -> bool:
        """
        Manages the return process by validating that the item belongs to the member.
        """
        member = self.find_member(member_id)
        item = self.find_item(item_id)

        if member and item and item_id in member.borrowed_items:
            item.return_item()
            member.borrowed_items.remove(item_id)
            return True
        return False

    # -----------------------------
    # PERSISTENCE
    # -----------------------------
    def save_to_json(self) -> None:
        """Serialises all members and items to the JSON persistence file."""

        data = {
            "members": [member.to_dict() for member in self.members],
            "items": [item.to_dict() for item in self.items],
        }
        with open(self.data_file, "w", encoding="utf-8") as file_handle:
            json.dump(data, file_handle, indent=2, ensure_ascii=False)

    def load_from_json(self) -> None:
        """Loads members and items from the JSON persistence file."""

        if not os.path.exists(self.data_file):
            return

        with open(self.data_file, "r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)

        self.members = [Member.from_dict(m) for m in data.get("members", [])]
        self.items = [Item.from_dict(i) for i in data.get("items", [])]


# ==============================================================================
# MODULE: main.py
# Entry point and menu flows
# Author: Ivan Bazhenov
# ==============================================================================

# from library import Library          # (combined into single file)
# from utils.validator import Validator  # (combined into single file)
# from utils.display import Display    # (combined into single file)


def items_menu_flow(library: Library) -> None:
    """Top-level Items menu: add or view items."""
    while True:
        Display.print_menu("Items Menu", ["Add a new item", "View all items"])
        choice = input("Choose an option: ")

        if choice == '1':
            print("Adding a new item...")

            title = input("Enter the item's title: ")
            while not Validator.validate_non_empty(title):
                Display.print_error("Title cannot be empty.")
                title = input("Enter the item's title: ")

            author = input("Enter the item's author: ")
            while not Validator.validate_non_empty(author):
                Display.print_error("Author cannot be empty.")
                author = input("Enter the item's author: ")

            item = library.add_item(title, author)
            library.save_to_json()
            Display.print_success(
                f"Item '{item.id}' with title '{item.title}' added successfully!"
            )

        elif choice == '2':
            all_items = library.get_all_items()
            if not all_items:
                Display.print_error("No items found.")
            else:
                Display.print_header("List of all items")
                Display.print_items_table(all_items)

        elif choice == '0':
            break
        else:
            Display.print_error("Invalid choice. Please try again.")

        input("<Press Enter to continue>")


def view_member_details(member) -> None:
    """Displays full personal details of a member."""
    Display.print_header(f"Details: {member.name}")
    print(f"  ID:        {member.id}")
    print(f"  Name:      {member.name}")
    print(f"  Email:     {member.email}")
    print(f"  Phone:     {member.phone}")
    print(f"  Birthdate: {member.birthdate}")


def view_member_borrowed_items(member, library: Library) -> None:
    """Displays a table of items currently borrowed by a member."""
    borrowed_ids = member.get_borrowed_items()
    if not borrowed_ids:
        Display.print_error("This member has no borrowed items.")
        return
    items = [library.find_item(iid) for iid in borrowed_ids if library.find_item(iid)]
    Display.print_header(f"Borrowed items: {member.name}")
    Display.print_items_table(items)


def borrow_item_flow(member, library: Library) -> None:
    """Lets a member borrow an available item."""
    available = library.get_available_items()
    if not available:
        Display.print_error("No items available for borrowing.")
        return

    Display.print_header("Available items")
    Display.print_items_table(available)

    item_id_str = input("Enter item ID to borrow (0 to cancel): ")
    if item_id_str == '0':
        return
    if not item_id_str.isdigit():
        Display.print_error("Invalid item ID.")
        return

    due_date = input("Enter due date (YYYY-MM-DD): ")
    while not Validator.validate_date(due_date):
        Display.print_error("Invalid date format. Use YYYY-MM-DD.")
        due_date = input("Enter due date (YYYY-MM-DD): ")

    if library.borrow_item(member.id, int(item_id_str), due_date):
        library.save_to_json()
        Display.print_success(f"Item borrowed successfully. Due: {due_date}")
    else:
        Display.print_error("Could not borrow item (not found or already borrowed).")


def return_item_flow(member, library: Library) -> None:
    """Lets a member return a borrowed item."""
    borrowed_ids = member.get_borrowed_items()
    if not borrowed_ids:
        Display.print_error("This member has no borrowed items to return.")
        return

    items = [library.find_item(iid) for iid in borrowed_ids if library.find_item(iid)]
    Display.print_header("Items to return")
    Display.print_items_table(items)

    item_id_str = input("Enter item ID to return (0 to cancel): ")
    if item_id_str == '0':
        return
    if not item_id_str.isdigit():
        Display.print_error("Invalid item ID.")
        return

    if library.return_item(member.id, int(item_id_str)):
        library.save_to_json()
        Display.print_success("Item returned successfully.")
    else:
        Display.print_error("Could not return item (not found or not borrowed by this member).")


def view_items_by_due_date(member, library: Library) -> None:
    """Shows a member's borrowed items grouped by due date."""
    borrowed_ids = member.get_borrowed_items()
    if not borrowed_ids:
        Display.print_error("This member has no borrowed items.")
        return

    grouped: dict = {}
    for iid in borrowed_ids:
        item = library.find_item(iid)
        if item:
            due = item.due_date or "No due date"
            grouped.setdefault(due, []).append(item)

    Display.print_header(f"Items by due date: {member.name}")
    Display.print_grouped_by_date(grouped)


def member_sub_menu(member, library: Library) -> None:
    """Sub-menu for a selected member: details, borrow, return, delete."""
    while True:
        Display.print_menu(
            f"Member: {member.name}",
            [
                "View details",
                "View borrowed items",
                "Borrow item",
                "Return item",
                "View items by due date",
                "Delete member",
            ],
        )
        choice = input("Choose an option: ")

        if choice == '1':
            view_member_details(member)
        elif choice == '2':
            view_member_borrowed_items(member, library)
        elif choice == '3':
            borrow_item_flow(member, library)
        elif choice == '4':
            return_item_flow(member, library)
        elif choice == '5':
            view_items_by_due_date(member, library)
        elif choice == '6':
            library.remove_member(member.id)
            library.save_to_json()
            Display.print_success(f"Member '{member.name}' deleted.")
            input("<Press Enter to continue>")
            break
        elif choice == '0':
            break
        else:
            Display.print_error("Invalid choice. Please try again.")

        input("<Press Enter to continue>")


def members_menu_flow(library: Library) -> None:
    """Top-level Members menu: add, view all, or drill into a member."""
    while True:
        Display.print_menu("Members Menu", ["Add a new member", "View all members"])
        choice = input("Choose an option: ")

        if choice == '1':
            print("Adding a new member...")

            name = input("Enter member name: ")
            while not Validator.validate_name(name):
                Display.print_error("Invalid name. Must be non-empty, max 50 characters.")
                name = input("Enter member name: ")

            email = input("Enter member email: ")
            while not Validator.validate_email(email):
                Display.print_error("Invalid email format.")
                email = input("Enter member email: ")

            phone = input("Enter member phone: ")
            while not Validator.validate_phone(phone):
                Display.print_error("Invalid phone number. Digits only, 7–15 chars.")
                phone = input("Enter member phone: ")

            birthdate = input("Enter member birthdate (YYYY-MM-DD): ")
            while not Validator.validate_date(birthdate):
                Display.print_error("Invalid birthdate. Use YYYY-MM-DD format.")
                birthdate = input("Enter member birthdate (YYYY-MM-DD): ")

            member = library.add_member(name, email, phone, birthdate)
            library.save_to_json()
            Display.print_success(
                f"Member '{member.id}' with name '{member.name}' added successfully!"
            )

        elif choice == '2':
            all_members = library.get_all_members()
            if not all_members:
                Display.print_error("No members found.")
            else:
                Display.print_header("List of all members")
                Display.print_members_table(all_members)
                member_id_str = input("\nEnter member ID for more options (0 to go back): ")
                if member_id_str != '0':
                    if member_id_str.isdigit():
                        member = library.find_member(int(member_id_str))
                        if member:
                            member_sub_menu(member, library)
                        else:
                            Display.print_error(f"Member ID {member_id_str} not found.")
                    else:
                        Display.print_error("Invalid input. Enter a numeric member ID.")

        elif choice == '0':
            break
        else:
            Display.print_error("Invalid choice. Please try again.")

        input("<Press Enter to continue>")


# ---------------------------------------------------------------------------
# TASK-10 — Main entry point (Ivan Bazhenov)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    library = Library()
    library.load_from_json()

    Display.print_header("Welcome to the Library Membership & Resource Management System")

    try:
        while True:
            Display.print_menu("Main Menu", ["Members", "Items"])
            choice = input("Choose an option: ")

            if choice == '1':
                members_menu_flow(library)
            elif choice == '2':
                items_menu_flow(library)
            elif choice == '0':
                library.save_to_json()
                Display.print_success("Goodbye! Data saved.")
                break
            else:
                Display.print_error("Invalid choice. Please enter 1, 2, or 0.")
                input("<Press Enter to continue>")

    except KeyboardInterrupt:
        library.save_to_json()
        print("\n")
        Display.print_success("Interrupted. Data saved. Goodbye!")
