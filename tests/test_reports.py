import pandas as pd
import pytest

from entities.transaction import Transaction
from library import Library
from reports import ReportService


@pytest.fixture
def reports_library():
    """A deterministic Library with enough data to exercise every report."""
    
    lib = Library()

    # 5 members across 4 faculties; year_level 1 has 2 members (Alice, Eve).
    for data in [
        ("Alice Brown", "alice@example.com", "0411", "2000-01-01", "Business", 1),
        ("Bob Smith", "bob@example.com", "0422", "2000-02-02", "Design", 2),
        ("Carol Jones", "carol@example.com", "0433", "2000-03-03", "Technology", 3),
        ("Dave White", "dave@example.com", "0444", "2000-04-04", "Health", 4),
        ("Eve Black", "eve@example.com", "0455", "2000-05-05", "Business", 1),
    ]:
        lib.add_member(*data)

    # 10 items: 3 Business, 2 Design, 2 Technology, 3 Health.
    for data in [
        ("B Book 1", "Author 1", "Business", 2010, 5),
        ("B Book 2", "Author 2", "Business", 2015, 3),
        ("B Book 3", "Author 3", "Business", 2022, 2),
        ("D Book 1", "Author 4", "Design", 2018, 4),
        ("D Book 2", "Author 5", "Design", 2024, 2),
        ("T Book 1", "Author 6", "Technology", 2012, 5),
        ("T Book 2", "Author 7", "Technology", 2020, 3),
        ("H Book 1", "Author 8", "Health", 2008, 2),
        ("H Book 2", "Author 9", "Health", 2019, 4),
        ("H Book 3", "Author 10", "Health", 2023, 3),
    ]:
        lib.add_item(*data)

    # 30 transactions, deterministic. Hand-built rather than via library.borrow_item
    # so we control return_date precisely (active vs returned-on-time vs returned-late).
    tx_specs = [
        # 3 active overdue (no return_date; due in past).
        (1, 1, 1, "2025-01-01", "2025-01-15", None),
        (2, 2, 4, "2025-02-01", "2025-02-15", None),
        (3, 3, 6, "2025-03-01", "2025-03-15", None),
        # 3 returned late (return_date > due_date).
        (4, 4, 8, "2025-04-01", "2025-04-15", "2025-04-20"),
        (5, 5, 9, "2025-05-01", "2025-05-15", "2025-05-25"),
        (6, 1, 2, "2025-06-01", "2025-06-15", "2025-06-22"),
    ]
    # 24 returned-on-time txns spread across 6 months, 4 per month.
    next_id = 7
    for m_idx, month in enumerate(
        ["2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]
    ):
        for j in range(4):
            member_id = (m_idx + j) % 5 + 1
            item_id = (m_idx * 4 + j) % 10 + 1
            tx_specs.append(
                (next_id, member_id, item_id, f"{month}-05", f"{month}-19", f"{month}-15")
            )
            next_id += 1

    for spec in tx_specs:
        lib.transactions.append(Transaction(*spec))

    # Propagate active loans into Item.borrowed_by / due_dates and Member.borrowed_items
    # so the catalog/availability reports match the transactions.
    for txn in lib.transactions:
        if not txn.is_active():
            continue
        item = lib.find_item(txn.item_id)
        member = lib.find_member(txn.member_id)
        if item is None or member is None:
            continue
        if txn.member_id not in item.borrowed_by:
            item.borrowed_by.append(txn.member_id)
            item.due_dates[txn.member_id] = txn.due_date
        if txn.item_id not in member.borrowed_items:
            member.borrowed_items.append(txn.item_id)

    return lib


# ---------- catalog_by_faculty ----------

def test_catalog_by_faculty_totals(reports_library):
    """books_count across all rows must sum to 10 (total items in fixture)."""
    
    df = ReportService(reports_library).catalog_by_faculty()
    assert set(df.columns) == {"faculty", "books_count", "total_copies", "available_copies"}
    assert df["books_count"].sum() == 10
    # 4 faculties present
    assert set(df["faculty"]) == {"Business", "Design", "Technology", "Health"}


def test_catalog_by_faculty_year_filter(reports_library):
    """year_from narrows the result to items >= year_from."""
    
    svc = ReportService(reports_library)
    full = svc.catalog_by_faculty()
    filtered = svc.catalog_by_faculty(year_from=2020)
    # Items with year >= 2020: B Book 3 (2022), D Book 2 (2024), T Book 2 (2020), H Book 3 (2023) → 4
    assert filtered["books_count"].sum() == 4
    assert filtered["books_count"].sum() < full["books_count"].sum()


# ---------- most_popular_books ----------

def test_most_popular_books_top_3(reports_library):
    """top_n=3 returns exactly 3 rows, sorted descending by borrow_count."""
    
    df = ReportService(reports_library).most_popular_books(top_n=3)
    assert list(df.columns) == ["item_id", "title", "author", "faculty", "borrow_count"]
    assert len(df) == 3
    assert df["borrow_count"].is_monotonic_decreasing


def test_most_popular_books_faculty_filter(reports_library):
    """faculty filter restricts results to that faculty's items only."""
    
    df = ReportService(reports_library).most_popular_books(faculty="Business", top_n=10)
    if not df.empty:
        assert (df["faculty"] == "Business").all()


# ---------- most_active_students ----------

def test_most_active_students_year_level_filter(reports_library):
    """year_level=1 narrows to Alice and Eve (the only members with year_level 1)."""
    df = ReportService(reports_library).most_active_students(year_level=1)
    assert list(df.columns) == ["member_id", "name", "faculty", "year_level", "borrow_count"]
    assert (df["year_level"] == 1).all()
    assert set(df["name"]).issubset({"Alice Brown", "Eve Black"})


def test_most_active_students_top_n_respected(reports_library):
    """top_n caps the row count even when more members would qualify."""
    df = ReportService(reports_library).most_active_students(top_n=2)
    assert len(df) <= 2


# ---------- overdue_loans ----------

def test_overdue_loans_distinguishes_statuses(reports_library):
    """Result must contain BOTH active_overdue and returned_late rows."""
    
    df = ReportService(reports_library).overdue_loans()
    assert list(df.columns) == [
        "txn_id", "member_name", "item_title",
        "due_date", "return_date", "days_late", "status",
    ]
    statuses = set(df["status"].unique())
    assert "active_overdue" in statuses
    assert "returned_late" in statuses
    # Active rows have NaN return_date; returned rows do not.
    active = df[df["status"] == "active_overdue"]
    returned = df[df["status"] == "returned_late"]
    assert active["return_date"].isna().all()
    assert returned["return_date"].notna().all()
    # 3 active overdue + 3 returned late = 6 rows from our seed.
    assert len(active) == 3
    assert len(returned) == 3


def test_overdue_loans_faculty_filter(reports_library):
    """Filtering by Business keeps only overdue rows whose item is Business."""
    
    df = ReportService(reports_library).overdue_loans(faculty="Business")
    # Active overdue txn 1 (item 1, Business) + returned-late txn 6 (item 2, Business) = 2 rows.
    assert len(df) == 2


# ---------- monthly_activity ----------

def test_monthly_activity_returns_sorted_dict(reports_library):
    """Keys must be in ascending order, formatted YYYY-MM."""
    
    data = ReportService(reports_library).monthly_activity()
    assert isinstance(data, dict)
    keys = list(data.keys())
    assert keys == sorted(keys)
    for k in keys:
        # YYYY-MM exactly 7 chars, with a dash at index 4
        assert len(k) == 7 and k[4] == "-"
        
    # All 30 transactions accounted for.
    assert sum(data.values()) == 30


def test_monthly_activity_date_range_filter(reports_library):
    """date_from/date_to narrows the dict to months strictly within the window."""
    
    data = ReportService(reports_library).monthly_activity(
        date_from="2025-04-01", date_to="2025-06-30",
    )
    assert set(data.keys()) == {"2025-04", "2025-05", "2025-06"}
    # 3 returned-late txns are in those months (one per month from our seed).
    assert sum(data.values()) == 3


# ---------- empty library safety ----------

def test_reports_handle_empty_library():
    """Every report must return an empty (but well-shaped) result on a fresh Library."""
    
    svc = ReportService(Library())
    assert svc.catalog_by_faculty().empty
    assert svc.most_popular_books().empty
    assert svc.most_active_students().empty
    assert svc.overdue_loans().empty
    assert svc.monthly_activity() == {}
