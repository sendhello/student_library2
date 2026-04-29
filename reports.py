from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from library import Library


class ReportService:
    """Builds the 5 A3 analytical reports from a Library snapshot."""

    def __init__(self, library: "Library"):
        self.library = library

    def _members_df(self) -> pd.DataFrame:
        """Members projection: id, name, email, faculty, year_level."""
        
        rows = [
            {
                "id": m.id,
                "name": m.name,
                "email": m.email,
                "faculty": m.faculty,
                "year_level": m.year_level,
            }
            for m in self.library.members
        ]
        return pd.DataFrame(
            rows, columns=["id", "name", "email", "faculty", "year_level"]
        )

    def _items_df(self) -> pd.DataFrame:
        """Items projection: id, title, author, faculty, year, copies, borrowed_count, available."""
        
        rows = [
            {
                "id": i.id,
                "title": i.title,
                "author": i.author,
                "faculty": i.faculty,
                "year": i.year,
                "copies": i.copies,
                "borrowed_count": len(i.borrowed_by),
                "available": i.copies - len(i.borrowed_by),
            }
            for i in self.library.items
        ]
        return pd.DataFrame(
            rows,
            columns=[
                "id", "title", "author", "faculty",
                "year", "copies", "borrowed_count", "available",
            ],
        )

    def _transactions_df(self) -> pd.DataFrame:
        """Transactions projection: id, member_id, item_id, borrow_date, due_date, return_date."""
        
        rows = [
            {
                "id": t.id,
                "member_id": t.member_id,
                "item_id": t.item_id,
                "borrow_date": t.borrow_date,
                "due_date": t.due_date,
                "return_date": t.return_date,
            }
            for t in self.library.transactions
        ]
        return pd.DataFrame(
            rows,
            columns=[
                "id", "member_id", "item_id",
                "borrow_date", "due_date", "return_date",
            ],
        )

    def catalog_by_faculty(
        self,
        year_from: int | None = None,
        year_to: int | None = None,
    ) -> pd.DataFrame:
        """Per-faculty catalogue: books_count, total_copies, available_copies."""
        
        df = self._items_df()
        if year_from is not None:
            df = df[df["year"] >= year_from]
        if year_to is not None:
            df = df[df["year"] <= year_to]

        if df.empty:
            return pd.DataFrame(
                columns=["faculty", "books_count", "total_copies", "available_copies"]
            )

        return (
            df.groupby("faculty", as_index=False)
              .agg(
                  books_count=("id", "count"),
                  total_copies=("copies", "sum"),
                  available_copies=("available", "sum"),
              )
              .sort_values("faculty")
              .reset_index(drop=True)
        )

    def most_popular_books(
        self,
        faculty: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        top_n: int = 10,
    ) -> pd.DataFrame:
        """Top-N items by borrow count, optionally filtered by faculty / date range."""
        
        txns = self._transactions_df()
        items = self._items_df()

        if faculty is not None:
            items = items[items["faculty"] == faculty]
            txns = txns[txns["item_id"].isin(items["id"])]
        if date_from is not None:
            txns = txns[txns["borrow_date"] >= date_from]
        if date_to is not None:
            txns = txns[txns["borrow_date"] <= date_to]

        columns = ["item_id", "title", "author", "faculty", "borrow_count"]
        if txns.empty:
            return pd.DataFrame(columns=columns)

        counts = (
            txns.groupby("item_id")
                .size()
                .reset_index(name="borrow_count")
        )
        joined = counts.merge(
            items[["id", "title", "author", "faculty"]].rename(columns={"id": "item_id"}),
            on="item_id",
            how="left",
        )
        return (
            joined.sort_values(
                ["borrow_count", "item_id"], ascending=[False, True]
            )
            .head(top_n)[columns]
            .reset_index(drop=True)
        )

    def most_active_students(
        self,
        faculty: str | None = None,
        year_level: int | None = None,
        top_n: int = 10,
    ) -> pd.DataFrame:
        """Top-N members by borrow count, optionally filtered by faculty / year level."""
        
        members = self._members_df()
        txns = self._transactions_df()

        if faculty is not None:
            members = members[members["faculty"] == faculty]
        if year_level is not None:
            members = members[members["year_level"] == year_level]
        txns = txns[txns["member_id"].isin(members["id"])]

        columns = ["member_id", "name", "faculty", "year_level", "borrow_count"]
        if txns.empty:
            return pd.DataFrame(columns=columns)

        counts = (
            txns.groupby("member_id")
                .size()
                .reset_index(name="borrow_count")
        )
        joined = counts.merge(
            members[["id", "name", "faculty", "year_level"]].rename(columns={"id": "member_id"}),
            on="member_id",
            how="left",
        )
        return (
            joined.sort_values(
                ["borrow_count", "member_id"], ascending=[False, True]
            )
            .head(top_n)[columns]
            .reset_index(drop=True)
        )

    def overdue_loans(self, faculty: str | None = None) -> pd.DataFrame:
        """All overdue loans — both currently active and returned late."""
        
        txns = self._transactions_df()
        items = self._items_df()
        members = self._members_df()

        if faculty is not None:
            allowed_item_ids = items[items["faculty"] == faculty]["id"]
            txns = txns[txns["item_id"].isin(allowed_item_ids)]

        columns = [
            "txn_id", "member_name", "item_title",
            "due_date", "return_date", "days_late", "status",
        ]
        if txns.empty:
            return pd.DataFrame(columns=columns)

        today_iso = date.today().isoformat()
        # end_date drives the overdue check: today for active, return_date for closed
        end_date = txns["return_date"].fillna(today_iso)
        overdue_mask = end_date > txns["due_date"]
        overdue = txns.loc[overdue_mask].copy()
        if overdue.empty:
            return pd.DataFrame(columns=columns)

        overdue["end_date"] = overdue["return_date"].fillna(today_iso)
        overdue["days_late"] = (
            pd.to_datetime(overdue["end_date"]) - pd.to_datetime(overdue["due_date"])
        ).dt.days
        overdue["status"] = overdue["return_date"].where(
            overdue["return_date"].isna(), "returned_late"
        ).fillna("active_overdue")

        joined = overdue.merge(
            members[["id", "name"]].rename(columns={"id": "member_id", "name": "member_name"}),
            on="member_id", how="left",
        ).merge(
            items[["id", "title"]].rename(columns={"id": "item_id", "title": "item_title"}),
            on="item_id", how="left",
        )
        joined = joined.rename(columns={"id": "txn_id"})
        return (
            joined[columns]
            .sort_values(["status", "days_late", "txn_id"], ascending=[True, False, True])
            .reset_index(drop=True)
        )

    def monthly_activity(
        self,
        faculty: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> dict[str, int]:
        """Borrow volume per `YYYY-MM`, sorted ascending. Feeds `Display.print_bar_chart`."""
        
        txns = self._transactions_df()
        items = self._items_df()

        if faculty is not None:
            allowed_item_ids = items[items["faculty"] == faculty]["id"]
            txns = txns[txns["item_id"].isin(allowed_item_ids)]
        if date_from is not None:
            txns = txns[txns["borrow_date"] >= date_from]
        if date_to is not None:
            txns = txns[txns["borrow_date"] <= date_to]

        if txns.empty:
            return {}

        months = txns["borrow_date"].str[:7]
        counts = months.value_counts().sort_index()
        return {str(month): int(n) for month, n in counts.items()}
