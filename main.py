from library import Library
from utils.validator import Validator
from utils.display import Display


## ----------------- RENATO'S PART BEGINS HERE ----------------------------
## -----------------------------------------------------------------------

def items_menu_flow(library):
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

            if hasattr(library, "save_to_json"):
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


## ----------------- YOUR PART BEGINS HERE ----------------------------
## -------------------------------------------------------------------

def members_menu_flow(library):
    while True:
        Display.print_menu("Members Menu", ["Add a new member", "View all members"])
        choice = input("Choose an option: ")

        if choice == '1':
            print("Adding a new member...")

            name = input("Enter member name: ")
            while not Validator.validate_non_empty(name):
                Display.print_error("Name cannot be empty.")
                name = input("Enter member name: ")

            birthdate = input("Enter member birthdate (YYYY-MM-DD): ")
            while not Validator.validate_date(birthdate):
                Display.print_error("Invalid birthdate. Use YYYY-MM-DD format.")
                birthdate = input("Enter member birthdate (YYYY-MM-DD): ")

            email = input("Enter member email: ")
            while not Validator.validate_email(email):
                Display.print_error("Invalid email format.")
                email = input("Enter member email: ")

            phone = input("Enter member phone: ")
            while not Validator.validate_phone(phone):
                Display.print_error("Invalid phone number.")
                phone = input("Enter member phone: ")

            member = library.add_member(name, birthdate, email, phone)

            if hasattr(library, "save_to_json"):
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
                for member in all_members:
                    print(member)

        elif choice == '0':
            break
        else:
            Display.print_error("Invalid choice. Please try again.")

        input("<Press Enter to continue>")



"""
# --- EXECUTION ZONE ---
if __name__ == "__main__":
    my_library = Library()
    print("Starting the test program...")
    items_menu_flow(my_library)
    print("Program completed.")
"""

"""
    

