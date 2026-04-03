"""Member class for representing library members."""
class Member:
    """
    Represents a library member.
    Stores personal details and borrowed items.
    """
    def __init__(self, member_id: int, name: str, email: str, phone: str):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_items = []

    def to_dict(self) -> dict:
        """Converts the instance into a dictionary for JSON storage."""
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "borrowed_items": self.borrowed_items
        }

    @staticmethod
    def from_dict(data: dict):
        """Creates a Member object from a data dictionary."""
        member = Member(
            data["member_id"],
            data["name"],
            data["email"],
            data["phone"]
        )
        member.borrowed_items = data.get("borrowed_items", [])
        return member

    def __str__(self):
        return f"Member ID: {self.member_id} | Name: {self.name} | Email: {self.email} | Phone: {self.phone}"

    def __repr__(self):
        return self.__str__()
      
