"""Member class for representing library members."""
from entities.base import BaseEntity


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
            "id": self.id,  # ✅ use BaseEntity property
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
        return f"Member ID: {self.id} | Name: {self.name} | Email: {self.email} | Phone: {self.phone} | Birthdate: {self.birthdate}"

    def __repr__(self) -> str:
        return self.__str__()

