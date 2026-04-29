# Student Library — Membership & Resource Management System

![Python](https://img.shields.io/badge/Python-3.11%2B-blue) ![Subject](https://img.shields.io/badge/MIS501-Assessment%203-orange)

A console-based library management system built in Python 3, developed for **MIS501 Principles of Programming — Assessment 3: Final Programming Solution with Data Integration** (Torrens University Australia).

---

## Scenario

> **Assessment 1 (Modules 1–4):** A single-user prototype built with fundamental Python only — variables, lists, dictionaries, `while` loops; no OOP, no files.
>
> **Assessment 2 (Modules 1–8):** That prototype was redesigned around object-oriented principles — modularity, encapsulation, abstraction — so the library could manage many members and items, with state persisted to a JSON file.

**Assessment 3 (Modules 1–11)** scales the system into a faculty-aware analytics application. The library now ingests external CSV data (students, books, six months of borrow history), tracks every loan as an immutable `Transaction`, and exposes five pandas-powered reports through a console menu. A custom exception hierarchy and a pytest suite back the codebase.

---

## Features

- Startup menu — bootstrap from `data.json`, import the bundled CSVs, or start empty
- Member management with **faculty** (Business / Design / Technology / Health) and **year level** (1–4)
- Item catalogue with faculty, publication year, and multi-copy tracking
- Borrow / return flows — every event recorded as a `Transaction` (append-only log)
- Transactions menu — view all, filter (member / item / date range / status), shortcuts for active and overdue
- **5 reports** powered by pandas: catalog by faculty, most popular books, most active students, overdue loans, monthly activity (ASCII bar chart)
- Custom exception hierarchy (`LibraryError`) with structured `try/except` at I/O boundaries
- 50 unit tests across validator / entities / library / data loader / reports

---

## How to run

**Requirements:** Python 3.11+

```bash
git clone <repo-url>
cd student_library2

python3 -m venv .venv
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\activate             # Windows

pip install -r requirements.txt
python main.py
```

On first launch (no `data.json` in the working directory), the application shows a startup menu:

```text
1. Import data from CSV (students.csv + books.csv + borrow_history.csv)
2. Start with an empty library
```

After import, the app keeps state in `data.json` (created automatically on save and reloaded on every subsequent launch). To start fresh, delete `data.json` and re-run.

The main menu has four sections — **Members**, **Items**, **Transactions**, **Reports**.

---

## Data

The `data/` folder ships with three deterministic CSV files used for first-time import:

| File | Rows | Columns |
| --- | --- | --- |
| `data/students.csv` | 80 | `student_id, name, email, phone, birthdate, faculty, year_level` |
| `data/books.csv` | 300 | `book_id, title, author, faculty, year, copies` |
| `data/borrow_history.csv` | 1000 | `transaction_id, student_id, book_id, borrow_date, due_date, return_date` |

History spans 2025-10-21 → 2026-04-21 with a triangular density (more recent months contain more events). The last ~100 rows have an empty `return_date` and represent loans currently held — `Library.import_from_csv()` propagates these into the matching `Member.borrowed_items` and `Item.borrowed_by` collections so the in-memory state is consistent with the log.

To regenerate the dataset (`random.seed(42)`, fully reproducible):

```bash
python scripts/generate_dataset.py
```

`data.json` is **not** committed (see `.gitignore`) — it is runtime state that the app rebuilds from the CSVs.

---

## Tests

The suite uses pytest. With dependencies installed, run from the repository root:

```bash
pytest -v
```

Coverage:

| File | Scope |
| --- | --- |
| `tests/test_validator.py` | All 7 validation rules (incl. faculty whitelist, year level 1..4) |
| `tests/test_member.py` | Construction, borrow/return state, dict round-trip |
| `tests/test_transaction.py` | `is_active`, `is_overdue`, `to_dict`/`from_dict` round-trip |
| `tests/test_library.py` | CRUD, borrow/return, cascade on `remove_member`, JSON persistence, `filter_transactions` |
| `tests/test_data_loader.py` | Schema check, leading-zero phone handling, malformed-row tolerance, missing file → `DataLoadError` |
| `tests/test_reports.py` | All 5 reports (totals, filters, sort order, status distinction) and empty-library safety |

UI flows in `main.py` are not unit-tested.

---

## Architecture

The system is organised as five layers, all console-only (no GUI):

1. **Entities** (`entities/`) — `BaseEntity` ABC plus `Member`, `Item`, `Transaction`. Round-trip through `to_dict`/`from_dict` for JSON persistence.
2. **Domain controller** (`library.py`) — `Library` owns three collections (`members`, `items`, `transactions`), enforces business rules (one copy per member per item, multi-copy availability, cascade close-out on member removal), and handles JSON save/load + CSV import.
3. **Data integration** (`data_loader.py`) — `DataLoader` parses the three CSVs into entity objects, validates schema, and tolerates malformed rows.
4. **Analytics** (`reports.py`) — `ReportService` builds 5 pandas DataFrames / dicts from a `Library` snapshot. Pure read-only; no mutation.
5. **Presentation & validation** (`utils/`) — `Validator` (static methods, faculty whitelist) and `Display` (menus, tables, ASCII bar chart). Top-level `main.py` wires everything into the menu.

Custom exceptions (`exceptions.py`) form a single hierarchy so callers can catch the base `LibraryError` at menu boundaries.

See [`student_library_class_diagram.drawio`](student_library_class_diagram.drawio) for the editable source.

![Class Diagram](student_library_class_diagram.png)

| Class | File | Responsibility |
| --- | --- | --- |
| `BaseEntity` | `entities/base.py` | Abstract base with `id` and `to_dict` / `from_dict` contract |
| `Member` | `entities/member.py` | Member data + `borrowed_items: list[int]`; faculty, year level |
| `Item` | `entities/item.py` | Item data + `borrowed_by: list[int]`, `due_dates: dict[int, str]`; multi-copy tracking |
| `Transaction` | `entities/transaction.py` | One borrow event; `is_active`, `is_overdue` |
| `Library` | `library.py` | Owns members/items/transactions; borrow/return, JSON persistence, CSV import, filter |
| `DataLoader` | `data_loader.py` | Parses 3 CSV files into entity lists; schema check + tolerant rows |
| `ReportService` | `reports.py` | 5 pandas reports built from a `Library` snapshot |
| `Validator` | `utils/validator.py` | Static input validators (name, email, phone, date, faculty, year level) |
| `Display` | `utils/display.py` | Console rendering (menus, tables, ASCII bar chart) |
| `LibraryError` (+ 5 subclasses) | `exceptions.py` | Custom exception hierarchy for all domain errors |

### Relationships

```text
Library  ──1:many──▶  Member
Library  ──1:many──▶  Item
Library  ──1:many──▶  Transaction
Member   ─ holds  ──▶  Item              (Member.borrowed_items / Item.borrowed_by)
Library  ─ uses ────▶  DataLoader        (CSV import)
ReportService ─ reads ▶ Library          (analytics, no mutation)
main.py  ─ uses ────▶  Validator, Display
```

---

## Flowchart

End-to-end console flow — startup menu, main menu loop, and the four sub-flows (Members, Items, Transactions, Reports). Saved alongside the code as `Flowchart.png`.

![Application Flowchart](Flowchart.png)

---

## Project structure

```text
student_library2/
├── main.py                              # Entry point, menus, startup flow
├── library.py                           # Library — domain controller
├── data_loader.py                       # CSV import
├── reports.py                           # ReportService — 5 pandas reports
├── exceptions.py                        # LibraryError hierarchy
├── entities/
│   ├── base.py                          # BaseEntity (ABC)
│   ├── member.py
│   ├── item.py
│   └── transaction.py
├── utils/
│   ├── validator.py                     # Validator (static methods)
│   └── display.py                       # Display (static methods)
├── data/                                # Bundled CSV dataset
│   ├── students.csv
│   ├── books.csv
│   └── borrow_history.csv
├── scripts/
│   └── generate_dataset.py              # Deterministic CSV generator (seed=42)
├── tests/                               # pytest suite
│   ├── conftest.py
│   ├── test_validator.py
│   ├── test_member.py
│   ├── test_transaction.py
│   ├── test_library.py
│   ├── test_data_loader.py
│   └── test_reports.py
├── requirements.txt
├── student_library_class_diagram.drawio
├── student_library_class_diagram.png
├── Flowchart.png
└── README.md
```

`data.json`, `__pycache__/`, `.pytest_cache/`, and `.venv/` are gitignored — they are runtime artefacts.

---

## Team

| Name | GitHub |
| --- | --- |
| Ivan Bazhenov (TL) | [@sendhello](https://github.com/sendhello) |
| Takunda Audrey Shelter | [@AudreyShelly3](https://github.com/AudreyShelly3) |
| Renato Bustamante | [@bustamantenate](https://github.com/bustamantenate) |

---

## Assessment context

| Field | Detail |
| --- | --- |
| Subject | MIS501 Principles of Programming |
| Assessment | Assessment 3 — Final Programming Solution with Data Integration |
| Institution | Torrens University Australia |
| Language | Python 3.11+ |
| External libraries | pandas (analytics), pytest (tests) |
| Concepts applied | OOP, inheritance + ABCs, file I/O, custom exceptions, CSV/JSON integration, unit testing, modular architecture |
| Modules covered | 1–11 |
