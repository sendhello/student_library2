if __name__ == "__main__":
    pass


## ----------------- RENATO'S PART BEGINS HERE ----------------------------
##----------------------------------------------------------------


# validator.py
class Validator:
    @staticmethod
    def get_non_empty_string(prompt: str) -> str:
        """Repeats the request until a valid (non-empty) text is obtained."""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Invalid input. This field cannot be empty.")

# Flow fragment in main.py
def items_menu_flow(library):
    while True:
        Display.print_menu("Items Menu", ["Add a new item", "View all items"])
        choice = input("Choose an option: ")

        if choice == '1':
            print("Adding a new item...")
            # Use Validator to ensure correct data
            title = Validator.get_non_empty_string("Enter the item's title: ")
            author = Validator.get_non_empty_string("Enter the item's author: ")
            
            item = library.add_item(title, author)
            library.save_to_json() # Requirement: save after adding
            Display.print_success(f"Item '{item.id}' with title '{item.title}' added successfully!")
            
        elif choice == '2':
            all_items = library.get_all_items()
            if not all_items:
                Display.print_error("No items found.")
            else:
                Display.print_header("List of all items")
                Display.print_items_table(all_items)
        
        elif choice == '0':
            break # '0' returns to the main menu
        else:
            Display.print_error("Invalid choice. Please try again.")
            
        input("<Press Enter to continue>")

##---------------------------------------------------------------------------------------------------
##------------------------- TEST  ------------------------------------------------------------

"""
# --- EXECUTION ZONE ---
if __name__ == "__main__":
    # 1. We instantiate the library
    mi_biblioteca = Library()

    # 2. CALL menu flow
    print("Starting the test program...")
    items_menu_flow(mi_biblioteca)
    
    print("Program completed.")

"""
    

