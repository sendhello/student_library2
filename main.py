from library import Library
from utils.validator import Validator
from utils.display import Display


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

            item = library.add_item(title, author)
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


def view_member_details(member) -> None:
    """Displays full personal details of a member."""
    Display.print_header(f"Details: {member.name}")
    print(f"  ID:        {member.id}")
    print(f"  Name:      {member.name}")
    print(f"  Email:     {member.email}")
    print(f"  Phone:     {member.phone}")
    print(f"  Birthdate: {member.birthdate}")


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

    if library.borrow_item(member.id, int(item_id_str), due_date):
        library.save_to_json()
        Display.print_success(f"Item borrowed successfully. Due: {due_date}")
    else:
        Display.print_error("Could not borrow item (not found or already borrowed).")


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

    if library.return_item(member.id, int(item_id_str)):
        library.save_to_json()
        Display.print_success("Item returned successfully.")
    else:
        Display.print_error("Could not return item (not found or not borrowed by this member).")


def view_items_by_due_date(member, library: Library) -> None:
    """Shows a member's borrowed items grouped by due date."""
    borrowed_ids = member.get_borrowed_items()
    if not borrowed_ids:
        Display.print_error("This member has no borrowed items.")
        return

    grouped: dict = {}
    for iid in borrowed_ids:
        item = library.find_item(iid)
        if item:
            due = item.due_date or "No due date"
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

            member = library.add_member(name, email, phone, birthdate)
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
# TASK-10 — Main entry point (Ivan Bazhenov)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    library = Library()
    library.load_from_json()

    Display.print_header("Welcome to the Library Membership & Resource Management System")

    try:
        while True:
            Display.print_menu("Main Menu", ["Members", "Items"])
            choice = input("Choose an option: ")

            if choice == '1':
                members_menu_flow(library)
            elif choice == '2':
                items_menu_flow(library)
            elif choice == '0':
                library.save_to_json()
                Display.print_success("Goodbye! Data saved.")
                break
            else:
                Display.print_error("Invalid choice. Please enter 1, 2, or 0.")
                input("<Press Enter to continue>")

    except KeyboardInterrupt:
        library.save_to_json()
        print("\n")
        Display.print_success("Interrupted. Data saved. Goodbye!")
