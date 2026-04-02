"""Item class for representing library items."""
# item.py

# item.py

class Item:
    """
    Represents a library resource.
    Handles the borrowing status and conversion to dictionaries for persistence.
    """
    def __init__(self, id: int, title: str, author: str):
        """Initializes an item with an ID, title, and author."""
        self.id = id
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

    @staticmethod
    def from_dict(data: dict):
        """Creates an Item object from a data dictionary."""
        item = Item(data['id'], data['title'], data['author'])
        item.borrowed_by = data.get('borrowed_by')
        item.due_date = data.get('due_date')
        return item

    def __str__(self):
        return f"Item ID: {self.id} | Title: {self.title} | Author: {self.author}"

    def __repr__(self):
        return self.__str__()


