"""A3 entry point: startup menu, member/item flows, transactions, reports."""
from exceptions import DataLoadError, LibraryError, PersistenceError
from library import Library
from reports import ReportService
from utils.display import Display
from utils.validator import Validator



def _prompt_faculty(label: str = "Choose a faculty") -> str:
    """Prompts the user to pick one of `Validator.FACULTIES` by index."""
    
    options = list(Validator.FACULTIES)
    while True:
        Display.print_menu(label, options)
        choice = input("Choose an option: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        Display.print_error(f"Invalid choice. Pick 1..{len(options)}.")


def _prompt_int(prompt: str, *, min_value: int, max_value: int | None = None) -> int:
    """Prompts for an integer in [min_value, max_value]; re-prompts on bad input."""
    
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            Display.print_error("Please enter a whole number.")
            continue
        if value < min_value or (max_value is not None and value > max_value):
            limit = f"{min_value}..{max_value}" if max_value is not None else f"≥ {min_value}"
            Display.print_error(f"Out of range. Expected {limit}.")
            continue
        return value


# ---------------------------------------------------------------------------
# Items menu
# ---------------------------------------------------------------------------

def items_menu_flow(library: Library) -> None:
    """Top-level Items menu: add or view items."""
    while True:
        Display.print_menu("Items Menu", ["Add a new item", "View all items"])
        choice = input("Choose an option: ")

        if choice == '1':
            print("Adding a new item...")

            title = input("Enter the item's title: ")
            while not Validator.validate_non_empty(title):
                Display.print_error("Title cannot be empty.")
                title = input("Enter the item's title: ")

            author = input("Enter the item's author: ")
            while not Validator.validate_non_empty(author):
                Display.print_error("Author cannot be empty.")
                author = input("Enter the item's author: ")

            faculty = _prompt_faculty("Faculty for this item")
            year = _prompt_int(
                "Enter publication year (2000..2026): ",
                min_value=2000, max_value=2026,
            )
            copies = _prompt_int("Enter number of copies (≥ 1): ", min_value=1)

            item = library.add_item(title, author, faculty, year, copies)
            library.save_to_json()
            Display.print_success(
                f"Item '{item.id}' with title '{item.title}' added successfully!"
            )

        elif choice == '2':
            all_items = library.get_all_items()
            if not all_items:
                Display.print_error("No items found.")
            else:
                Display.print_header("List of all items")
                Display.print_items_table(all_items)

        elif choice == '0':
            break
        else:
            Display.print_error("Invalid choice. Please try again.")

        input("<Press Enter to continue>")


# ---------------------------------------------------------------------------
# Members — sub-flows
# ---------------------------------------------------------------------------

def view_member_details(member) -> None:
    """Displays full personal details of a member."""
    Display.print_header(f"Details: {member.name}")
    print(f"  ID:         {member.id}")
    print(f"  Name:       {member.name}")
    print(f"  Email:      {member.email}")
    print(f"  Phone:      {member.phone}")
    print(f"  Birthdate:  {member.birthdate}")
    print(f"  Faculty:    {member.faculty}")
    print(f"  Year level: {member.year_level}")


def view_member_borrowed_items(member, library: Library) -> None:
    """Displays a table of items currently borrowed by a member."""
    borrowed_ids = member.get_borrowed_items()
    if not borrowed_ids:
        Display.print_error("This member has no borrowed items.")
        return
    items = [library.find_item(iid) for iid in borrowed_ids if library.find_item(iid)]
    Display.print_header(f"Borrowed items: {member.name}")
    Display.print_items_table(items)


def borrow_item_flow(member, library: Library) -> None:
    """Lets a member borrow an available item."""
    available = library.get_available_items()
    if not available:
        Display.print_error("No items available for borrowing.")
        return

    Display.print_header("Available items")
    Display.print_items_table(available)

    item_id_str = input("Enter item ID to borrow (0 to cancel): ")
    if item_id_str == '0':
        return
    if not item_id_str.isdigit():
        Display.print_error("Invalid item ID.")
        return

    due_date = input("Enter due date (YYYY-MM-DD): ")
    while not Validator.validate_date(due_date):
        Display.print_error("Invalid date format. Use YYYY-MM-DD.")
        due_date = input("Enter due date (YYYY-MM-DD): ")

    library.borrow_item(member.id, int(item_id_str), due_date)
    library.save_to_json()
    Display.print_success(f"Item borrowed successfully. Due: {due_date}")


def return_item_flow(member, library: Library) -> None:
    """Lets a member return a borrowed item."""
    borrowed_ids = member.get_borrowed_items()
    if not borrowed_ids:
        Display.print_error("This member has no borrowed items to return.")
        return

    items = [library.find_item(iid) for iid in borrowed_ids if library.find_item(iid)]
    Display.print_header("Items to return")
    Display.print_items_table(items)

    item_id_str = input("Enter item ID to return (0 to cancel): ")
    if item_id_str == '0':
        return
    if not item_id_str.isdigit():
        Display.print_error("Invalid item ID.")
        return

    library.return_item(member.id, int(item_id_str))
    library.save_to_json()
    Display.print_success("Item returned successfully.")


def view_items_by_due_date(member, library: Library) -> None:
    """Shows a member's borrowed items grouped by their due date."""
    borrowed_ids = member.get_borrowed_items()
    if not borrowed_ids:
        Display.print_error("This member has no borrowed items.")
        return

    grouped: dict[str, list] = {}
    for iid in borrowed_ids:
        item = library.find_item(iid)
        if not item:
            continue
        # A3: per-copy due dates live in Item.due_dates[member_id]
        due = item.due_dates.get(member.id, "No due date")
        grouped.setdefault(due, []).append(item)

    Display.print_header(f"Items by due date: {member.name}")
    Display.print_grouped_by_date(grouped)


def member_sub_menu(member, library: Library) -> None:
    """Sub-menu for a selected member: details, borrow, return, delete."""
    while True:
        Display.print_menu(
            f"Member: {member.name}",
            [
                "View details",
                "View borrowed items",
                "Borrow item",
                "Return item",
                "View items by due date",
                "Delete member",
            ],
        )
        choice = input("Choose an option: ")

        if choice == '1':
            view_member_details(member)
        elif choice == '2':
            view_member_borrowed_items(member, library)
        elif choice == '3':
            borrow_item_flow(member, library)
        elif choice == '4':
            return_item_flow(member, library)
        elif choice == '5':
            view_items_by_due_date(member, library)
        elif choice == '6':
            library.remove_member(member.id)
            library.save_to_json()
            Display.print_success(f"Member '{member.name}' deleted.")
            input("<Press Enter to continue>")
            break
        elif choice == '0':
            break
        else:
            Display.print_error("Invalid choice. Please try again.")

        input("<Press Enter to continue>")


def members_menu_flow(library: Library) -> None:
    """Top-level Members menu: add, view all, or drill into a member."""
    
    while True:
        Display.print_menu("Members Menu", ["Add a new member", "View all members"])
        choice = input("Choose an option: ")

        if choice == '1':
            print("Adding a new member...")

            name = input("Enter member name: ")
            while not Validator.validate_name(name):
                Display.print_error("Invalid name. Must be non-empty, max 50 characters.")
                name = input("Enter member name: ")

            email = input("Enter member email: ")
            while not Validator.validate_email(email):
                Display.print_error("Invalid email format.")
                email = input("Enter member email: ")

            phone = input("Enter member phone: ")
            while not Validator.validate_phone(phone):
                Display.print_error("Invalid phone number. Digits only, 7–15 chars.")
                phone = input("Enter member phone: ")

            birthdate = input("Enter member birthdate (YYYY-MM-DD): ")
            while not Validator.validate_date(birthdate):
                Display.print_error("Invalid birthdate. Use YYYY-MM-DD format.")
                birthdate = input("Enter member birthdate (YYYY-MM-DD): ")

            faculty = _prompt_faculty("Faculty for this member")
            year_level = _prompt_int("Enter year level (1..4): ", min_value=1, max_value=4)

            member = library.add_member(name, email, phone, birthdate, faculty, year_level)
            library.save_to_json()
            Display.print_success(
                f"Member '{member.id}' with name '{member.name}' added successfully!"
            )

        elif choice == '2':
            all_members = library.get_all_members()
            if not all_members:
                Display.print_error("No members found.")
            else:
                Display.print_header("List of all members")
                Display.print_members_table(all_members)
                member_id_str = input("\nEnter member ID for more options (0 to go back): ")
                if member_id_str != '0':
                    if member_id_str.isdigit():
                        member = library.find_member(int(member_id_str))
                        if member:
                            member_sub_menu(member, library)
                        else:
                            Display.print_error(f"Member ID {member_id_str} not found.")
                    else:
                        Display.print_error("Invalid input. Enter a numeric member ID.")

        elif choice == '0':
            break
        else:
            Display.print_error("Invalid choice. Please try again.")

        input("<Press Enter to continue>")


# ---------------------------------------------------------------------------
# Transactions menu
# ---------------------------------------------------------------------------

def _prompt_optional_int(prompt: str) -> int | None:
    """Prompts for an int. Empty input → None. Re-prompts on bad input."""
    
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            Display.print_error("Please enter a whole number, or leave blank for any.")


def _prompt_optional_date(prompt: str) -> str | None:
    """Prompts for a YYYY-MM-DD date. Empty input → None. Re-prompts on bad input."""
    
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        if Validator.validate_date(raw):
            return raw
        Display.print_error("Invalid date. Use YYYY-MM-DD, or leave blank for any.")


def _prompt_status() -> str | None:
    """Maps numeric status choice (1..4) to filter_transactions status string."""
    
    options = ["Any", "Active", "Returned", "Overdue"]
    mapping = [None, "active", "returned", "overdue"]
    while True:
        Display.print_menu("Status", options)
        raw = input("Choose an option: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return mapping[int(raw) - 1]
        Display.print_error(f"Invalid choice. Pick 1..{len(options)}.")


def _filter_transactions_subflow(library: Library) -> None:
    """Prompts for each filter (blank = any) and renders the matched transactions."""
    
    print("Leave any field blank to ignore that filter.")
    member_id = _prompt_optional_int("Filter by member ID: ")
    item_id = _prompt_optional_int("Filter by item ID: ")
    date_from = _prompt_optional_date("Borrow date from (YYYY-MM-DD): ")
    date_to = _prompt_optional_date("Borrow date to (YYYY-MM-DD): ")
    status = _prompt_status()

    txns = library.filter_transactions(
        member_id=member_id,
        item_id=item_id,
        date_from=date_from,
        date_to=date_to,
        status=status,
    )
    Display.print_header(f"Filtered transactions ({len(txns)})")
    Display.print_transactions_table(txns, library)


def transactions_menu_flow(library: Library) -> None:
    """Top-level Transactions menu: view / filter / active / overdue."""
    
    while True:
        Display.print_menu(
            "Transactions Menu",
            [
                "View all transactions",
                "Filter transactions",
                "View active loans only",
                "View overdue loans",
            ],
        )
        choice = input("Choose an option: ")

        if choice == '1':
            txns = library.get_all_transactions()
            Display.print_header(f"All transactions ({len(txns)})")
            Display.print_transactions_table(txns, library)
        elif choice == '2':
            _filter_transactions_subflow(library)
        elif choice == '3':
            txns = library.filter_transactions(status="active")
            Display.print_header(f"Active loans ({len(txns)})")
            Display.print_transactions_table(txns, library)
        elif choice == '4':
            txns = library.filter_transactions(status="overdue")
            Display.print_header(f"Overdue loans ({len(txns)})")
            Display.print_transactions_table(txns, library)
        elif choice == '0':
            break
        else:
            Display.print_error("Invalid choice. Please try again.")

        input("<Press Enter to continue>")


# ---------------------------------------------------------------------------
# Reports menu
# ---------------------------------------------------------------------------

def _prompt_optional_faculty(label: str = "Filter by faculty") -> str | None:
    """Numbered faculty picker with `Any` as the first option."""
    
    options = ["Any (no filter)", *Validator.FACULTIES]
    while True:
        Display.print_menu(label, options)
        raw = input("Choose an option: ").strip()
        if raw.isdigit():
            idx = int(raw)
            if idx == 1:
                return None
            if 2 <= idx <= len(options):
                return options[idx - 1]
        Display.print_error(f"Invalid choice. Pick 1..{len(options)}.")


def _prompt_optional_year_level() -> int | None:
    """Blank → None (any). Numeric → must satisfy `Validator.validate_year_level`."""
    
    while True:
        raw = input("Filter by year level (1..4, blank = any): ").strip()
        if raw == "":
            return None
        if Validator.validate_year_level(raw):
            return int(raw)
        Display.print_error("Invalid year level. Use 1..4, or leave blank for any.")


def _prompt_top_n(default: int = 10) -> int:
    """Blank → default. Numeric ≥ 1. Re-prompts on bad input."""
    
    while True:
        raw = input(f"Top N (blank = {default}): ").strip()
        if raw == "":
            return default
        try:
            n = int(raw)
        except ValueError:
            Display.print_error("Please enter a whole number, or leave blank for default.")
            continue
        if n < 1:
            Display.print_error("Top N must be at least 1.")
            continue
        return n


def _render_dataframe_report(df, title: str) -> None:
    """Adapter from pandas DataFrame to `Display.print_report_table`."""
    
    Display.print_report_table(df.to_dict("records"), df.columns.tolist(), title)


def reports_menu_flow(library: Library) -> None:
    """Top-level Reports menu wired to ReportService."""
    
    svc = ReportService(library)
    while True:
        Display.print_menu(
            "Reports Menu",
            [
                "Catalog by faculty",
                "Most popular books",
                "Most active students",
                "Overdue loans",
                "Monthly loan activity",
            ],
        )
        choice = input("Choose an option: ")

        if choice == '1':
            year_from = _prompt_optional_int("Year from (blank = any): ")
            year_to = _prompt_optional_int("Year to (blank = any): ")
            df = svc.catalog_by_faculty(year_from=year_from, year_to=year_to)
            _render_dataframe_report(df, "Catalog by faculty")
            
        elif choice == '2':
            faculty = _prompt_optional_faculty("Faculty filter")
            date_from = _prompt_optional_date("Borrow date from (YYYY-MM-DD, blank = any): ")
            date_to = _prompt_optional_date("Borrow date to (YYYY-MM-DD, blank = any): ")
            top_n = _prompt_top_n()
            df = svc.most_popular_books(
                faculty=faculty, date_from=date_from, date_to=date_to, top_n=top_n,
            )
            _render_dataframe_report(df, "Most popular books")
            
        elif choice == '3':
            faculty = _prompt_optional_faculty("Faculty filter")
            year_level = _prompt_optional_year_level()
            top_n = _prompt_top_n()
            df = svc.most_active_students(
                faculty=faculty, year_level=year_level, top_n=top_n,
            )
            _render_dataframe_report(df, "Most active students")
            
        elif choice == '4':
            faculty = _prompt_optional_faculty("Faculty filter")
            df = svc.overdue_loans(faculty=faculty)
            _render_dataframe_report(df, "Overdue loans")
            
        elif choice == '5':
            faculty = _prompt_optional_faculty("Faculty filter")
            date_from = _prompt_optional_date("Borrow date from (YYYY-MM-DD, blank = any): ")
            date_to = _prompt_optional_date("Borrow date to (YYYY-MM-DD, blank = any): ")
            data = svc.monthly_activity(
                faculty=faculty, date_from=date_from, date_to=date_to,
            )
            Display.print_bar_chart(data, "Monthly loan activity")
            
        elif choice == '0':
            break
        
        else:
            Display.print_error("Invalid choice. Please try again.")

        input("<Press Enter to continue>")


# ---------------------------------------------------------------------------
# Startup flow
# ---------------------------------------------------------------------------

def initial_setup(library: Library) -> None:
    """Two-option setup: import the bundled CSVs, or start empty."""
    while True:
        Display.print_menu(
            "Initial setup",
            [
                "Import data from CSV (students.csv + books.csv + borrow_history.csv)",
                "Start with an empty library",
            ],
        )
        choice = input("Choose an option: ").strip()

        if choice == '1':
            try:
                library.import_from_csv(
                    "data/students.csv",
                    "data/books.csv",
                    "data/borrow_history.csv",
                )
                library.save_to_json()
                Display.print_success(
                    f"Imported {len(library.members)} members, "
                    f"{len(library.items)} items, "
                    f"{len(library.transactions)} transactions."
                )
            except DataLoadError as e:
                Display.print_error(f"Import failed: {e}")
                Display.print_error("Falling back to an empty library.")
            return
        elif choice == '2':
            return
        else:
            Display.print_error("Invalid choice. Please pick 1 or 2.")


def bootstrap_library() -> Library:
    """Loads `data.json` if available; otherwise runs the initial-setup menu."""
    library = Library()
    try:
        loaded = library.load_from_json()
    except PersistenceError as e:
        Display.print_error(f"Could not read data.json: {e}")
        loaded = False

    if not loaded or library.is_empty():
        initial_setup(library)

    return library


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    Display.print_header("Welcome to the Library Membership & Resource Management System")

    library = bootstrap_library()

    try:
        while True:
            try:
                Display.print_menu(
                    "Main Menu", ["Members", "Items", "Transactions", "Reports"]
                )
                choice = input("Choose an option: ")

                if choice == '1':
                    members_menu_flow(library)
                elif choice == '2':
                    items_menu_flow(library)
                elif choice == '3':
                    transactions_menu_flow(library)
                elif choice == '4':
                    reports_menu_flow(library)
                elif choice == '0':
                    library.save_to_json()
                    Display.print_success("Goodbye! Data saved.")
                    break
                else:
                    Display.print_error("Invalid choice. Please enter 1, 2, 3, 4, or 0.")
                    input("<Press Enter to continue>")
            except LibraryError as e:
                Display.print_error(str(e))
                input("<Press Enter to continue>")

    except KeyboardInterrupt:
        library.save_to_json()
        print("\n")
        Display.print_success("Interrupted. Data saved. Goodbye!")
