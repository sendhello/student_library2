"""Item class for representing library items."""
from entities.base import BaseEntity
from typing import Dict, List, Optional

class Item(BaseEntity):
    """
    Represents a library resource.
    Handles the borrowing status and conversion to dictionaries for persistence.
    """

    def __init__(self, item_id: int, title: str, author: str, faculty: str, year: int, copies: int):
        """Initializes an item with an ID, title, author, faculty, year, and number of copies."""
        super().__init__(item_id)
        self.title = title
        self.author = author
        self.faculty = faculty
        self.year = year
        self.copies = copies
        self.borrowed_by: List[int] = []  # Stores member IDs currently holding a copy
        self.due_dates: Dict[int, str] = {}  # Maps member_id to due date

    def is_available(self) -> bool:
        """Checks if at least one copy is available."""
        return len(self.borrowed_by) < self.copies

    def available_copies(self) -> int:
        """Returns the number of available copies."""
        return self.copies - len(self.borrowed_by)

    def borrow(self, member_id: int, due_date: str) -> bool:
        """
        Assigns a copy of the item to a member and sets the due date.
        Returns False if no copies are available or if the member already holds a copy.
        """
        if not self.is_available():
            return False
        if member_id in self.borrowed_by:
            return False

        self.borrowed_by.append(member_id)
        self.due_dates[member_id] = due_date
        return True

    def return_item(self, member_id: int) -> bool:
        """
        Marks a copy of the item as returned.
        Returns False if the member is not currently holding a copy.
        """
        if member_id not in self.borrowed_by:
            return False

        self.borrowed_by.remove(member_id)
        del self.due_dates[member_id]
        return True

    def to_dict(self) -> dict:
        """Converts the instance into a dictionary for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "faculty": self.faculty,
            "year": self.year,
            "copies": self.copies,
            "borrowed_by": self.borrowed_by,
            "due_dates": self.due_dates
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        """Creates an Item object from a data dictionary."""
        item = cls(
            data['id'],
            data['title'],
            data['author'],
            data['faculty'],
            data['year'],
            data['copies']
        )
        item.borrowed_by = data.get('borrowed_by', [])
        item.due_dates = data.get('due_dates', {})
        return item

    def __str__(self) -> str:
        """Returns a human-readable string representation."""
        return f"Item ID: {self.id} | Title: {self.title} | Author: {self.author} | Faculty: {self.faculty} | Year: {self.year} | Copies: {self.copies}"
