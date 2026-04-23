"""Library module for managing library items and members."""
# library.py (Clase Library enriquecida)



##--------------------------------------------------------------------------------
## -------------- PART 2 ---------------------------------------------------
## Implement class Library — item & borrowing management (library.py, part 2)


import json
import os

from entities.transaction import Transaction
from entities.member import Member
from entities.item import Item

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
            member_id=member_id,
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
            item_id=item_id,
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
        return [item for item in self.items if item.is_available()]

    def get_all_transactions(self):
        return self.transactions

    def get_active_transactions(self):
        return [txn for txn in self.transactions if txn.is_active()]
