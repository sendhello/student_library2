"""Member class for representing library members."""
class Member:
    def __init__(self, member_id, name, email, phone):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_items = []

    def borrow_item(self, item):
        """Add an item to borrowed list"""
        self.borrowed_items.append(item)

    def return_item(self, item):
        """Remove an item from borrowed list"""
        if item in self.borrowed_items:
            self.borrowed_items.remove(item)

    def display_info(self):
        """Display member information"""
        print(f"\nMember ID: {self.member_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone}")
        print(f"Borrowed Items: {self.borrowed_items}")
