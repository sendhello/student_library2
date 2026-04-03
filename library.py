"""Library module for managing library items and members."""
# library.py (Clase Library enriquecida)



##--------------------------------------------------------------------------------
## -------------- PART 2 ---------------------------------------------------
## Implement class Library — item & borrowing management (library.py, part 2)


from entities.item import Item
from entities.member import Member


class Library:
    def __init__(self):
        self.members = []
        self.items = []

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
    def add_member(self, name: str, email: str, phone: str):
        """Creates, adds, and returns a new Member instance."""
        new_id = len(self.members) + 1
        new_member = Member(new_id, name.strip().title(), email.strip(), phone.strip())
        self.members.append(new_member)
        return new_member

    def find_member(self, member_id: int):
        """Searches for a member by ID. Returns None if it does not exist."""
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def get_all_members(self) -> list:
        """Returns the complete list of members."""
        return self.members

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









