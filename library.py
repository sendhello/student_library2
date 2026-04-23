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

class NotFoundError(Exception):
    """Raised when a member or item is not found."""
    pass

class BorrowingError(Exception):
    """Raised when an item cannot be borrowed or returned."""
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
        today = datetime.date.today().isoformat()
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

        today = datetime.date.today().isoformat()
        transaction = active_txns[0]
        transaction.return_date = today
        return transaction

    def remove_member(self, member_id: int) -> bool:
        member = self.find_member(member_id)
        if not member:
            raise NotFoundError(f"Member with ID {member_id} not found.")

        today = datetime.date.today().isoformat()
        for txn in self.transactions:
            if txn.member_id == member_id and txn.is_active():
                txn.return_date = today
                item = self.find_item(txn.item_id)
                if item:
                    item.return_item()

        self.members = [m for m in self.members if m.id != member_id]
        return True
