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
            # Supports both Member objects (m.id) and dictionaries (m['id'])
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
