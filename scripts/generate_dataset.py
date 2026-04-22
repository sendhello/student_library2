"""Generate the 3 CSV files for Assessment 3 data integration.

Deterministic (seed=42). Run once per dataset regeneration:

    python scripts/generate_dataset.py

Produces three files under data/:
    - students.csv           (80 records)
    - books.csv              (300 records)
    - borrow_history.csv     (1000 records over 2025-10-21 .. 2026-04-21)

This script is a development utility and is NOT part of the submission bundle.
Stdlib-only (random, csv, datetime, pathlib) so it runs without any virtualenv.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

FACULTIES = ["Business", "Design", "Technology", "Health"]
YEAR_LEVELS = [1, 2, 3, 4]

PERIOD_START = date(2025, 10, 21)
PERIOD_END = date(2026, 4, 21)
LOAN_DAYS = 14
TARGET_ACTIVE_LOANS = 100  # approximate; final count depends on capacity

MONTHLY_DENSITY = [
    # (year, month, days_in_window, record_count)
    (2025, 10, 11, 55),     # Oct 21..31
    (2025, 11, 30, 110),
    (2025, 12, 31, 140),
    (2026, 1, 31, 150),
    (2026, 2, 28, 180),
    (2026, 3, 31, 220),
    (2026, 4, 21, 145),     # Apr 1..21
]

FIRST_NAMES = [
    "Aarav", "Ada", "Adrian", "Alice", "Amir", "Anya", "Arjun", "Ashley",
    "Beatrice", "Benjamin", "Caleb", "Camille", "Chen", "Chloe", "Daniel",
    "Diana", "Ethan", "Evelyn", "Farhan", "Fatima", "Gabriel", "Grace",
    "Hiroshi", "Hiromi", "Ibrahim", "Isabella", "Jason", "Jasmine", "Kai",
    "Kiara", "Lachlan", "Laila", "Marcus", "Mei", "Nathan", "Noor",
    "Oliver", "Olivia", "Pablo", "Priya", "Quentin", "Rachel", "Ravi",
    "Samantha", "Santiago", "Sophia", "Takumi", "Tara", "Umar", "Uma",
    "Vincent", "Valentina", "Wesley", "Willow", "Xander", "Xiao",
    "Yasmin", "Yuki", "Zachary", "Zara",
]

LAST_NAMES = [
    "Anderson", "Baker", "Chen", "Davis", "Evans", "Fernandez", "Garcia",
    "Hassan", "Ivanov", "Jackson", "Kim", "Lopez", "Martin", "Nguyen",
    "O'Brien", "Patel", "Quinn", "Roberts", "Singh", "Tanaka", "Uchida",
    "Vargas", "Williams", "Xu", "Yamamoto", "Zhang", "Brown", "Cooper",
    "Dixon", "Ellis", "Ford", "Green", "Hughes", "Ito", "Jones", "Khan",
    "Lee", "Morgan", "Novak", "Okafor", "Park", "Reyes", "Silva", "Turner",
    "Volkov", "Walker", "Wong", "Young",
]

# Title templates: two-part composition yields ~250+ unique combos per faculty.
TITLE_PATTERNS = [
    "Introduction to {topic}",
    "Advanced {topic}",
    "Principles of {topic}",
    "The {topic} Handbook",
    "Foundations of {topic}",
    "Mastering {topic}",
    "{topic} in Practice",
    "{topic}: A Modern Approach",
    "{topic} for Professionals",
    "Applied {topic}",
    "{topic} and Society",
    "Understanding {topic}",
    "Exploring {topic}",
    "Essential {topic}",
    "The Art of {topic}",
    "Contemporary {topic}",
    "{topic}: Theory and Practice",
    "The Science of {topic}",
    "{topic} Research Methods",
    "Thinking in {topic}",
    "Beyond {topic}",
    "Frontiers of {topic}",
    "{topic}: Concepts and Cases",
    "{topic} Fundamentals",
]

TOPICS_BY_FACULTY = {
    "Business": [
        "Marketing", "Finance", "Accounting", "Management", "Strategy",
        "Entrepreneurship", "Leadership", "Economics", "Negotiation",
        "Operations", "Supply Chain", "Corporate Governance", "Branding",
        "Organisational Behaviour", "Project Management",
    ],
    "Design": [
        "Graphic Design", "Typography", "User Experience", "Interaction Design",
        "Visual Communication", "Design Thinking", "Industrial Design",
        "Colour Theory", "Design History", "Motion Graphics", "Illustration",
        "Service Design", "Branding Systems", "Photography", "3D Modelling",
    ],
    "Technology": [
        "Software Engineering", "Algorithms", "Data Structures", "Databases",
        "Web Development", "Cloud Computing", "Cybersecurity", "Networks",
        "Operating Systems", "Artificial Intelligence", "Machine Learning",
        "Computer Graphics", "Distributed Systems", "Data Engineering",
        "Quantum Computing",
    ],
    "Health": [
        "Public Health", "Nursing Practice", "Anatomy", "Physiology",
        "Nutrition", "Pharmacology", "Epidemiology", "Mental Health",
        "Paediatrics", "Clinical Research", "Health Informatics",
        "Biomedical Ethics", "Gerontology", "Rehabilitation", "Global Health",
    ],
}

AUTHORS = [
    "J. Smith", "M. Chen", "R. Patel", "A. Garcia", "S. Anderson", "L. Nguyen",
    "K. O'Connor", "T. Kowalski", "P. Silva", "H. Tanaka", "N. Dubois",
    "D. Williams", "I. Volkov", "O. Olsson", "E. Cohen", "Y. Park", "B. Fischer",
    "C. Morales", "F. Khan", "V. Rossi", "G. Martin", "W. Zhao", "X. Suzuki",
    "U. Erdogan", "Q. Rahman", "Z. Abebe", "J. Okafor", "R. Singh", "A. Lopez",
    "M. Johansson", "P. Antoniou", "N. Iqbal", "L. Becker", "T. Hoffmann",
    "E. Novak", "S. Andersson", "K. Hassan", "D. Roy", "C. Schneider",
    "B. McCarthy",
]


def _rand_date(rng: random.Random, start: date, end: date) -> date:
    """Uniform random date in [start, end]."""
    delta = (end - start).days
    return start + timedelta(days=rng.randint(0, delta))


def _email(first: str, last: str, suffix: str = "") -> str:
    base = f"{first}.{last}".lower().replace("'", "")
    return f"{base}{suffix}@torrens.edu.au"


def generate_students(rng: random.Random, n: int = 80) -> list[dict]:
    """Generate n unique students."""
    used_emails: set[str] = set()
    students: list[dict] = []
    for student_id in range(1, n + 1):
        first = rng.choice(FIRST_NAMES)
        last = rng.choice(LAST_NAMES)
        email = _email(first, last)
        suffix_i = 1
        while email in used_emails:
            suffix_i += 1
            email = _email(first, last, suffix=str(suffix_i))
        used_emails.add(email)

        phone = "04" + "".join(str(rng.randint(0, 9)) for _ in range(8))

        # Age 18..30 → born 1996..2008
        birth_year = rng.randint(1996, 2008)
        birth_month = rng.randint(1, 12)
        birth_day = rng.randint(1, 28)
        birthdate = date(birth_year, birth_month, birth_day).isoformat()

        faculty = rng.choice(FACULTIES)
        year_level = rng.choice(YEAR_LEVELS)

        students.append({
            "student_id": student_id,
            "name": f"{first} {last}",
            "email": email,
            "phone": phone,
            "birthdate": birthdate,
            "faculty": faculty,
            "year_level": year_level,
        })
    return students


def generate_books(rng: random.Random, n: int = 300) -> list[dict]:
    """Generate n books balanced across faculties."""
    faculty_cycle = (FACULTIES * ((n // len(FACULTIES)) + 1))[:n]
    rng.shuffle(faculty_cycle)

    used_titles: set[str] = set()
    books: list[dict] = []
    for book_id in range(1, n + 1):
        faculty = faculty_cycle[book_id - 1]
        topics = TOPICS_BY_FACULTY[faculty]
        # Try a few times to avoid duplicate titles within same faculty
        for _ in range(20):
            pattern = rng.choice(TITLE_PATTERNS)
            topic = rng.choice(topics)
            title = pattern.format(topic=topic)
            if title not in used_titles:
                used_titles.add(title)
                break
        else:
            title = f"{title} (Vol. {book_id})"
            used_titles.add(title)

        author = rng.choice(AUTHORS)
        year = rng.randint(2010, 2025)
        copies = rng.randint(1, 5)

        books.append({
            "book_id": book_id,
            "title": title,
            "author": author,
            "faculty": faculty,
            "year": year,
            "copies": copies,
        })
    return books


def _compute_return_date(rng: random.Random, due: date) -> date:
    """Return date: normally due ±3 days; 5% significantly overdue (+10..+30)."""
    if rng.random() < 0.05:
        offset = rng.randint(10, 30)
    else:
        offset = rng.randint(-3, 3)
    return due + timedelta(days=offset)


def generate_history(rng: random.Random, students: list[dict], books: list[dict],
                     target_total: int = 1000) -> list[dict]:
    """Generate borrow_history with triangular monthly density and active tail.

    Approach:
    1. Generate target_total transactions with borrow_date sampled within
       each month's window to match MONTHLY_DENSITY.
    2. Sort by borrow_date ascending; assign sequential transaction_ids.
    3. Compute due_date = borrow_date + 14d; return_date per _compute_return_date.
    4. Walk the most-recent tail; mark transactions as active (return_date = "")
       while respecting per-book copy capacity and per-(student, book) uniqueness
       for active loans. Stop once ~TARGET_ACTIVE_LOANS actives marked.
    """
    transactions: list[dict] = []
    for year, month, days, count in MONTHLY_DENSITY:
        start = date(year, month, 1) if month != 10 else date(2025, 10, 21)
        end_day = start.day + days - 1
        end = date(year, month, end_day)
        for _ in range(count):
            borrow = _rand_date(rng, start, end)
            student = rng.choice(students)
            book = rng.choice(books)
            transactions.append({
                "_borrow_date": borrow,
                "student_id": student["student_id"],
                "book_id": book["book_id"],
            })

    # Sort by date so ids match chronological order
    transactions.sort(key=lambda t: t["_borrow_date"])
    # Trim/pad to exact target_total
    transactions = transactions[:target_total]

    rows: list[dict] = []
    for idx, raw in enumerate(transactions, start=1):
        borrow = raw["_borrow_date"]
        due = borrow + timedelta(days=LOAN_DAYS)
        ret = _compute_return_date(rng, due)
        rows.append({
            "transaction_id": idx,
            "student_id": raw["student_id"],
            "book_id": raw["book_id"],
            "borrow_date": borrow.isoformat(),
            "due_date": due.isoformat(),
            "return_date": ret.isoformat(),
        })

    # Mark tail as active, respecting capacity
    book_copies = {b["book_id"]: b["copies"] for b in books}
    active_by_book: dict[int, int] = {}
    active_student_book: set[tuple[int, int]] = set()
    active_count = 0
    # Walk the last N*2 tail so we have headroom if some fail capacity check
    for row in reversed(rows[-min(len(rows), TARGET_ACTIVE_LOANS * 3):]):
        if active_count >= TARGET_ACTIVE_LOANS:
            break
        book_id = row["book_id"]
        student_id = row["student_id"]
        key = (student_id, book_id)
        if key in active_student_book:
            continue
        if active_by_book.get(book_id, 0) >= book_copies[book_id]:
            continue
        row["return_date"] = ""          # "" = active (NULL in CSV)
        active_by_book[book_id] = active_by_book.get(book_id, 0) + 1
        active_student_book.add(key)
        active_count += 1

    return rows


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    """Write rows to CSV with given column order."""
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rng = random.Random(SEED)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    students = generate_students(rng)
    books = generate_books(rng)
    history = generate_history(rng, students, books)

    write_csv(
        DATA_DIR / "students.csv",
        students,
        ["student_id", "name", "email", "phone", "birthdate", "faculty", "year_level"],
    )
    write_csv(
        DATA_DIR / "books.csv",
        books,
        ["book_id", "title", "author", "faculty", "year", "copies"],
    )
    write_csv(
        DATA_DIR / "borrow_history.csv",
        history,
        ["transaction_id", "student_id", "book_id", "borrow_date", "due_date", "return_date"],
    )

    actives = sum(1 for r in history if r["return_date"] == "")
    print(f"Generated {len(students)} students -> {DATA_DIR / 'students.csv'}")
    print(f"Generated {len(books)} books       -> {DATA_DIR / 'books.csv'}")
    print(f"Generated {len(history)} transactions -> {DATA_DIR / 'borrow_history.csv'}")
    print(f"  Active loans (return_date empty): {actives}")


if __name__ == "__main__":
    main()
