"""Library module for managing library items and members."""
# library.py (Clase Library enriquecida)


##--------------------------------------------------------------------------------
## -------------- PART 2 ---------------------------------------------------
## Implement class Library — item & borrowing management (library.py, part 2)


import json
import os

from entities.item import Item
from entities.member import Member
from entities.transaction import Transaction
from datetime import datetime
import json
import os

class NotFoundError(Exception):
    """Raised when a member or item is not found."""
    pass

class BorrowingError(Exception):
    """Raised when an item cannot be borrowed or returned."""
    pass

class PersistenceError(Exception):
    """Raised when there is an error saving or loading data."""
    pass

class Library:
    def __init__(self):
        self.members = []
        self.items = []
        self.transactions = []

    def _next_member_id(self):
        return max((member.id for member in self.members), default=0) + 1

    def _next_item_id(self):
        return max((item.id for item in self.items), default=0) + 1

    def _next_txn_id(self):
        return max((txn.id for txn in self.transactions), default=0) + 1

    def add_member(self, name, email, phone, birthdate, faculty, year_level):
        member_id = self._next_member_id()
        member = Member(
            id=member_id,
            name=name,
            email=email,
            phone=phone,
            birthdate=birthdate,
            faculty=faculty,
            year_level=year_level
        )
        self.members.append(member)
        return member

    def add_item(self, title, author, faculty, year, copies):
        item_id = self._next_item_id()
        item = Item(
            id=item_id,
            title=title,
            author=author,
            faculty=faculty,
            year=year,
            copies=copies
        )
        self.items.append(item)
        return item

    def find_member(self, member_id):
        for member in self.members:
            if member.id == member_id:
                return member
        return None

    def find_item(self, item_id):
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def find_transaction(self, txn_id):
        for txn in self.transactions:
            if txn.id == txn_id:
                return txn
        return None

    def get_all_members(self):
        return self.members

    def get_all_items(self):
        return self.items

    def get_available_items(self):
        return [item for item in self.items if item.available_copies > 0]

    def get_all_transactions(self):
        return self.transactions

    def get_active_transactions(self):
        return [txn for txn in self.transactions if txn.is_active()]

    def borrow_item(self, member_id: int, item_id: int, due_date: str) -> Transaction:
        member = self.find_member(member_id)
        item = self.find_item(item_id)
        if not member:
            raise NotFoundError(f"Member with ID {member_id} not found.")
        if not item:
            raise NotFoundError(f"Item with ID {item_id} not found.")

        if not item.is_available():
            raise BorrowingError(f"No available copies of item {item_id}.")
        if item_id in member.get_borrowed_items():
            raise BorrowingError(f"Member {member_id} already holds item {item_id}.")

        item.borrow(member_id, due_date)
        member.borrow_item(item_id)

        txn_id = self._next_txn_id()
        today = datetime.now().date().isoformat()
        transaction = Transaction(
            id=txn_id,
            member_id=member_id,
            item_id=item_id,
            borrow_date=today,
            due_date=due_date
        )
        self.transactions.append(transaction)
        return transaction

    def return_item(self, member_id: int, item_id: int) -> Transaction:
        member = self.find_member(member_id)
        item = self.find_item(item_id)
        if not member:
            raise NotFoundError(f"Member with ID {member_id} not found.")
        if not item:
            raise NotFoundError(f"Item with ID {item_id} not found.")

        active_txns = [
            txn for txn in self.transactions
            if txn.member_id == member_id and txn.item_id == item_id and txn.is_active()
        ]
        if not active_txns:
            raise BorrowingError(f"No active transaction for member {member_id} and item {item_id}.")

        item.return_item()
        member.return_item(item_id)

        today = datetime.now().date().isoformat()
        transaction = active_txns[0]
        transaction.return_date = today
        return transaction

    def remove_member(self, member_id: int) -> bool:
        member = self.find_member(member_id)
        if not member:
            raise NotFoundError(f"Member with ID {member_id} not found.")

        today = datetime.now().date().isoformat()
        for txn in self.transactions:
            if txn.member_id == member_id and txn.is_active():
                txn.return_date = today
                item = self.find_item(txn.item_id)
                if item:
                    item.return_item()

        self.members = [m for m in self.members if m.id != member_id]
        return True

    def save_to_json(self, file_path: str) -> None:
        """Save the library data to a JSON file."""
        data = {
            "members": [member.to_dict() for member in self.members],
            "items": [item.to_dict() for item in self.items],
            "transactions": [txn.to_dict() for txn in self.transactions]
        }
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except OSError as e:
            raise PersistenceError(f"Error saving to {file_path}: {e}")

    def load_from_json(self, file_path: str) -> bool:
        """Load the library data from a JSON file."""
        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            self.members = [Member.from_dict(member_data) for member_data in data.get("members", [])]
            self.items = [Item.from_dict(item_data) for item_data in data.get("items", [])]
            self.transactions = [Transaction.from_dict(txn_data) for txn_data in data.get("transactions", [])]

            return len(self.members) > 0 or len(self.items) > 0 or len(self.transactions) > 0
        except (OSError, json.JSONDecodeError) as e:
            raise PersistenceError(f"Error loading from {file_path}: {e}")

    def is_empty(self) -> bool:
        """Check if the library is empty."""
        return len(self.members) == 0 and len(self.items) == 0 and len(self.transactions) == 0

    def filter_transactions(
        self,
        member_id: int | None = None,
        item_id: int | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        status: str | None = None
    ) -> list[Transaction]:
        """Filter transactions based on the given criteria."""
        filtered = self.transactions

        if member_id is not None:
            filtered = [txn for txn in filtered if txn.member_id == member_id]
        if item_id is not None:
            filtered = [txn for txn in filtered if txn.item_id == item_id]
        if date_from is not None:
            filtered = [txn for txn in filtered if txn.borrow_date >= date_from]
        if date_to is not None:
            filtered = [txn for txn in filtered if txn.borrow_date <= date_to]
        if status is not None:
            today = datetime.now().date().isoformat()
            if status == "active":
                filtered = [txn for txn in filtered if txn.is_active()]
            elif status == "returned":
                filtered = [txn for txn in filtered if not txn.is_active()]
            elif status == "overdue":
                filtered = [txn for txn in filtered if txn.is_active() and txn.due_date < today]

        return filtered

    def import_from_csv(self, students_path: str, books_path: str, history_path: str) -> None:
        """Import data from CSV files using DataLoader."""
        try:
            # Asumimos que DataLoader es una clase que maneja la importación desde CSV
            loader = DataLoader()
            self.members = loader.load_students(students_path)
            self.items = loader.load_books(books_path)
            self.transactions = loader.load_history(history_path)
        except Exception as e:
            raise e  # Propagamos cualquier error de DataLoader
