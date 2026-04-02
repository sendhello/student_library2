if __name__ == "__main__":
    pass


## ----------------- HERE RENATO START ----------------------------
##----------------------------------------------------------------


class Validator:
    @staticmethod
    def get_non_empty_string(prompt: str) -> str:
        """Repite la solicitud hasta obtener un texto válido (no vacío)."""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Invalid input. This field cannot be empty.")

# Fragmento del flujo en main.py
def items_menu_flow(library):
    while True:
        Display.print_menu("Items Menu", ["Add a new item", "View all items"])
        choice = input("Choose an option: ")

        if choice == '1':
            print("Adding a new item...")
            # Uso de Validator para asegurar datos correctos
            title = Validator.get_non_empty_string("Enter the item's title: ")
            author = Validator.get_non_empty_string("Enter the item's author: ")
            
            item = library.add_item(title, author)
            library.save_to_json() # Requerimiento: guardar tras agregar
            Display.print_success(f"Item '{item.id}' with title '{item.title}' added successfully!")
            
        elif choice == '2':
            all_items = library.get_all_items()
            if not all_items:
                Display.print_error("No items found.")
            else:
                Display.print_header("List of all items")
                Display.print_items_table(all_items)
        
        elif choice == '0':
            break # '0' vuelve al menú principal
        else:
            Display.print_error("Invalid choice. Please try again.")
            
        input("<Press Enter to continue>")

##---------------------------------------------------------------------------------------------------
##------------------------- PRUEBAS ------------------------------------------------------------

"""
# --- ZONA DE EJECUCIÓN ---
if __name__ == "__main__":
    # 1. Instanciamos la biblioteca
    mi_biblioteca = Library()

    # 2. Llamamos al flujo del menú de ítems
    print("Iniciando el programa de prueba...")
    items_menu_flow(mi_biblioteca)
    
    print("Programa finalizado.")

"""
    

