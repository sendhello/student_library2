from library import Library
from utils.validator import Validator
from utils.display import Display   # change this if your display file is elsewhere


## ----------------- RENATO'S PART BEGINS HERE ----------------------------
##----------------------------------------------------------------

def items_menu_flow(library):
    while True:
        Display.print_menu("Items Menu", ["Add a new item", "View all items"])
        choice = input("Choose an option: ")

        if choice == '1':
            print("Adding a new item...")
            title = Validator.get_non_empty_string("Enter the item's title: ")
            author = Validator.get_non_empty_string("Enter the item's author: ")

            item = library.add_item(title, author)

            if hasattr(library, "save_to_json"):
                library.save_to_json()

            Display.print_success(f"Item '{item.id}' with title '{item.title}' added successfully!")

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
##----------------------------------------------------------------

def members_menu_flow(library):
    while True:
        Display.print_menu("Members Menu", ["Add a new member", "View all members"])
        choice = input("Choose an option: ")

        if choice == '1':
            print("Adding a new member...")

            name = Validator.get_non_empty_string("Enter member name: ")
            email = Validator.get_non_empty_string("Enter member email: ")
            phone = Validator.get_non_empty_string("Enter member phone: ")

            if not Validator.validate_name(name):
                Display.print_error("Invalid name.")
            elif not Validator.validate_email(email):
                Display.print_error("Invalid email format.")
            elif not Validator.validate_phone(phone):
                Display.print_error("Invalid phone number.")
            else:
                member = library.add_member(name, email, phone)

                if hasattr(library, "save_to_json"):
                    library.save_to_json()

                Display.print_success(
                    f"Member '{member.member_id}' with name '{member.name}' added successfully!"
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
    

