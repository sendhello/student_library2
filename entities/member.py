"""Member class for representing library members."""
from entities.base import BaseEntity


class Member(BaseEntity):
    """
    Represents a library member.
    Stores personal details and borrowed items.
    """

    def __init__(
        self,
        member_id: int,
        name: str,
        email: str,
        phone: str,
        birthdate: str,
        faculty: str,
        year_level: int
    ):
        super().__init__(member_id)
        self.name = name
        self.birthdate = birthdate
        self.email = email
        self.phone = phone
        self.faculty = faculty
        self.year_level = year_level
        self.borrowed_items = []

    def borrow_item(self, item_id: int) -> None:
        if item_id not in self.borrowed_items:
            self.borrowed_items.append(item_id)

    def return_item(self, item_id: int) -> None:
        if item_id in self.borrowed_items:
            self.borrowed_items.remove(item_id)

    def get_borrowed_items(self) -> list:
        return self.borrowed_items

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "birthdate": self.birthdate,
            "email": self.email,
            "phone": self.phone,
            "faculty": self.faculty,
            "year_level": self.year_level,
            "borrowed_items": self.borrowed_items
        }

    @classmethod
    def from_dict(cls, data: dict):
        member = cls(
            member_id=data["id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            birthdate=data["birthdate"],
            faculty=data.get("faculty", "Unknown"),     # safe default
            year_level=data.get("year_level", 1)        # safe default
        )
        member.borrowed_items = data.get("borrowed_items", [])
        return member

    def __str__(self) -> str:
        return (
            f"Member ID: {self.id} | Name: {self.name} | "
            f"Email: {self.email} | Phone: {self.phone} | "
            f"Birthdate: {self.birthdate} | "
            f"Faculty: {self.faculty} | Year: {self.year_level}"
        )

    def __repr__(self) -> str:
        return self.__str__()
