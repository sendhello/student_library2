import pandas as pd

from entities.item import Item
from entities.member import Member
from entities.transaction import Transaction
from exceptions import DataLoadError


class DataLoader:
    """Reads the three A3 CSV files into entity lists."""

    EXPECTED_STUDENT_COLS = {
        "student_id", "name", "email", "phone",
        "birthdate", "faculty", "year_level",
    }
    EXPECTED_BOOK_COLS = {
        "book_id", "title", "author", "faculty", "year", "copies",
    }
    EXPECTED_HIST_COLS = {
        "transaction_id", "student_id", "book_id",
        "borrow_date", "due_date", "return_date",
    }

    def load_students(self, path: str) -> list[Member]:
        """Parses students CSV into Member objects. Skips malformed rows."""

        df = self._read_csv(path, dtype={"phone": str})
        self._check_schema(df, self.EXPECTED_STUDENT_COLS, path)

        members: list[Member] = []
        for idx, row in df.iterrows():
            try:
                member = Member(
                    member_id=int(row["student_id"]),
                    name=str(row["name"]),
                    email=str(row["email"]),
                    phone=str(row["phone"]),
                    birthdate=str(row["birthdate"]),
                    faculty=str(row["faculty"]),
                    year_level=int(row["year_level"]),
                )
                members.append(member)
            except (ValueError, TypeError) as e:
                print(f"Warning: skipped row {idx} in {path}: {e}")
        return members

    def load_books(self, path: str) -> list[Item]:
        """Parses books CSV into Item objects. Skips malformed rows."""

        df = self._read_csv(path)
        self._check_schema(df, self.EXPECTED_BOOK_COLS, path)

        items: list[Item] = []
        for idx, row in df.iterrows():
            try:
                item = Item(
                    item_id=int(row["book_id"]),
                    title=str(row["title"]),
                    author=str(row["author"]),
                    faculty=str(row["faculty"]),
                    year=int(row["year"]),
                    copies=int(row["copies"]),
                )
                items.append(item)
            except (ValueError, TypeError) as e:
                print(f"Warning: skipped row {idx} in {path}: {e}")
                
        return items

    def load_history(self, path: str) -> list[Transaction]:
        """Parses borrow_history CSV into Transaction objects.

        Empty `return_date` cells (NaN in pandas) become Python `None`,
        signalling an active loan.
        """
        df = self._read_csv(path, dtype={"return_date": str})
        self._check_schema(df, self.EXPECTED_HIST_COLS, path)

        transactions: list[Transaction] = []
        for idx, row in df.iterrows():
            try:
                raw_return = row["return_date"]
                # pandas reads empty cells as NaN even with dtype=str
                return_date = (
                    None
                    if pd.isna(raw_return) or str(raw_return).strip() == ""
                    else str(raw_return)
                )
                txn = Transaction(
                    transaction_id=int(row["transaction_id"]),
                    member_id=int(row["student_id"]),
                    item_id=int(row["book_id"]),
                    borrow_date=str(row["borrow_date"]),
                    due_date=str(row["due_date"]),
                    return_date=return_date,
                )
                transactions.append(txn)
            except (ValueError, TypeError) as e:
                print(f"Warning: skipped row {idx} in {path}: {e}")
                
        return transactions

    @staticmethod
    def _read_csv(path: str, dtype: dict | None = None) -> pd.DataFrame:
        """Reads a CSV, wrapping I/O and parser errors as DataLoadError."""

        try:
            return pd.read_csv(path, dtype=dtype)
        except FileNotFoundError as e:
            raise DataLoadError(f"File not found: {path}") from e
        except pd.errors.EmptyDataError as e:
            raise DataLoadError(f"Empty CSV file: {path}") from e
        except pd.errors.ParserError as e:
            raise DataLoadError(f"Could not parse CSV {path}: {e}") from e

    @staticmethod
    def _check_schema(df: pd.DataFrame, expected: set[str], path: str) -> None:
        """Raises DataLoadError if required columns are missing."""

        missing = expected - set(df.columns)
        if missing:
            raise DataLoadError(
                f"Missing required columns in {path}: {sorted(missing)}"
            )
