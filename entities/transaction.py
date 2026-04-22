"""Transaction class representing a single borrow event."""
from entities.base import BaseEntity
from typing import Self


class Transaction(BaseEntity):
    """Represents a single borrow event linking a Member to an Item.

    Append-only analytics log. Not the source of truth for current borrow
    state (that stays on Member.borrowed_items and Item.borrowed_by).
    All dates use the 'YYYY-MM-DD' string format so lexicographic
    comparison matches chronological order.
    """

    def __init__(
        self,
        transaction_id: int,
        member_id: int,
        item_id: int,
        borrow_date: str,
        due_date: str,
        return_date: str | None = None,
    ):
        super().__init__(transaction_id)
        self.member_id = member_id
        self.item_id = item_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = return_date  # None means the loan is active

    def is_active(self) -> bool:
        """Returns True when the loan has not been returned yet."""

        return self.return_date is None

    def is_overdue(self, today: str) -> bool:
        """
        Returns True when the loan ended past its due date.

        For active loans, compares `today` vs `due_date`.
        For returned loans, compares `return_date` vs `due_date`.
        """
        end_date = self.return_date if self.return_date is not None else today
        return end_date > self.due_date

    def to_dict(self) -> dict:
        """Converts the instance into a dictionary for JSON storage."""

        return {
            "id": self.id,
            "member_id": self.member_id,
            "item_id": self.item_id,
            "borrow_date": self.borrow_date,
            "due_date": self.due_date,
            "return_date": self.return_date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Creates a Transaction from a data dictionary."""

        return cls(
            transaction_id=data["id"],
            member_id=data["member_id"],
            item_id=data["item_id"],
            borrow_date=data["borrow_date"],
            due_date=data["due_date"],
            return_date=data.get("return_date"),
        )

    def __str__(self) -> str:
        """Returns a human-readable string representation."""

        status = "active" if self.is_active() else f"returned {self.return_date}"
        return (
            f"Transaction ID: {self.id} | Member: {self.member_id} | "
            f"Item: {self.item_id} | Borrowed: {self.borrow_date} | "
            f"Due: {self.due_date} | Status: {status}"
        )
