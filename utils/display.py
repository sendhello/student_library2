"""Display module for handling display of library items and members."""
# utils/display.py
# utils/display.py

# utils/display.py


class Display:
    """Static class for the console user interface."""

    @staticmethod
    def print_header(title: str) -> None:
        """Prints a decorated title bar."""
        print("\n" + "-" * 70)
        print(f"{title.upper():^70}")
        print("-" * 70)

    @staticmethod
    def print_menu(title: str, options: list[str]) -> None:
        """Prints a numbered menu based on a list of options."""
        Display.print_header(title)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("0. Back")

    @staticmethod
    def print_members_table(members: list) -> None:
        """Displays the members table using the original format from library.py."""
        print(f"| {'Member ID':10} | {'Name':20} | {'Email':30} | {'Phone':15} | {'Birthdate':12} |")
        print("-" * 100)
        for m in members:
            mid = m.id if hasattr(m, 'id') else m['id']
            name = m.name if hasattr(m, 'name') else m['name']
            email = m.email if hasattr(m, 'email') else m['email']
            phone = m.phone if hasattr(m, 'phone') else m['phone']
            bd = m.birthdate if hasattr(m, 'birthdate') else m['birthdate']
            print(f"| {mid:10} | {name:20} | {email:30} | {phone:15} | {bd:12} |")
        print("-" * 100)

    @staticmethod
    def print_items_table(items: list) -> None:
        """Displays the items table with availability status."""
        print(f"| {'Item ID':10} | {'Title':38} | {'Author':30} | {'Status':10} |")
        print("-" * 100)
        for item in items:
            status = "Borrowed" if not item.is_available() else "Available"
            print(f"| {item.id:10} | {item.title:38} | {item.author:30} | {status:10} |")
        print("-" * 100)

    @staticmethod
    def print_grouped_by_date(grouped: dict) -> None:
        """Prints items grouped by their due date."""
        for date, items in grouped.items():
            print(f"\nDue Date: {date}")
            print(f"| {'Item ID':10} | {'Title':40} | {'Author':30} |")
            print("-" * 90)
            for item in items:
                print(f"| {item.id:10} | {item.title:40} | {item.author:30} |")
            print("-" * 90)

    @staticmethod
    def print_success(msg: str) -> None:
        """Displays a success message."""
        print(f"\n>>> SUCCESS: {msg}")

    @staticmethod
    def print_error(msg: str) -> None:
        """Displays an error message."""
        print(f"\n!!! ERROR: {msg}")

    @staticmethod
    def print_transactions_table(transactions: list, library) -> None:
        """Prints a table of transactions with 7 columns: ID | Member | Item | Borrowed | Due | Returned | Status."""
        if not transactions:
            print("No transactions to display.")
            return

        print(f"| {'ID':6} | {'Member':20} | {'Item':45} | {'Borrowed':10} | {'Due':10} | {'Returned':10} | {'Status':10} |")
        print("-" * 133)

        for txn in transactions:
            member = library.find_member(txn.member_id)
            item = library.find_item(txn.item_id)

            member_name = member.name if member else "Unknown"
            item_title = item.title if item else "Unknown"

            status = "active" if txn.is_active() else ("overdue" if txn.return_date and txn.return_date > txn.due_date else "returned")

            print(f"| {txn.id:6} | {member_name:20} | {item_title:45} | {txn.borrow_date:10} | {txn.due_date:10} | {txn.return_date if txn.return_date else '':10} | {status:10} |")

        print("-" * 133)

    @staticmethod
    def print_report_table(rows: list[dict], columns: list[str], title: str) -> None:
        """Prints a generic table from a list of dictionaries with variable columns."""
        if not rows:
            print(f"No {title.lower()} to display.")
            return

        Display.print_header(title)

        # Calculate column widths
        col_widths = {}
        for col in columns:
            col_widths[col] = max(6, min(40, len(col)))

        for row in rows:
            for col in columns:
                if col in row:
                    col_widths[col] = max(col_widths[col], min(40, len(str(row[col]))))

        # Print header
        header = " | ".join(f"{col:<{col_widths[col]}}" for col in columns)
        print(header)
        print("-" * len(header))

        # Print rows
        for row in rows:
            row_str = " | ".join(f"{str(row.get(col, '')):<{col_widths[col]}}" for col in columns)
            print(row_str)

        print("-" * len(header))

    @staticmethod
    def print_bar_chart(data: dict, title: str, max_width: int = 40) -> None:
        """Prints an ASCII bar chart with the given data."""
        if not data:
            print("No data to display.")
            return

        Display.print_header(title)

        max_value = max(data.values())
        scale = max_width / max_value if max_value != 0 else 1

        for label, value in data.items():
            bar_length = int(value * scale)
            bar = '#' * bar_length
            print(f"{label:10} | {bar:<{max_width}} {value}")
