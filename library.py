"""Library module for managing library items and members."""
# library.py (Clase Library enriquecida)



##--------------------------------------------------------------------------------
## -------------- PART 2 ---------------------------------------------------
## Implement class Library — item & borrowing management (library.py, part 2)


import json
import os

from entities.item import Item
from entities.member import Member


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
