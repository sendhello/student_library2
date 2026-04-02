"""Display module for handling display of library items and members."""
# utils/display.py

class Display:
    """Clase estática para la interfaz de usuario por consola."""

    @staticmethod
    def print_header(title: str) -> None:
        """Imprime una barra de título decorada."""
        print("\n" + "-" * 70)
        print(f"{title.upper():^70}")
        print("-" * 70)

    @staticmethod
    def print_menu(title: str, options: list[str]) -> None:
        """Imprime un menú numerado basado en una lista de opciones."""
        Display.print_header(title)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("0. Volver")

    @staticmethod
    def print_members_table(members: list) -> None:
        """Muestra la tabla de miembros con el formato original del library.py."""
        print(f"| {'Member ID':10} | {'Name':20} | {'Email':30} | {'Phone':15} | {'Birthdate':12} |")
        print("-" * 100)
        for m in members:
            # Soporta tanto objetos Member (m.id) como diccionarios (m['id'])
            mid = m.id if hasattr(m, 'id') else m['id']
            name = m.name if hasattr(m, 'name') else m['name']
            email = m.email if hasattr(m, 'email') else m['email']
            phone = m.phone if hasattr(m, 'phone') else m['phone']
            bd = m.birthdate if hasattr(m, 'birthdate') else m['birthdate']
            print(f"| {mid:10} | {name:20} | {email:30} | {phone:15} | {bd:12} |")
        print("-" * 100)

    @staticmethod
    def print_items_table(items: list) -> None:
        """Muestra la tabla de ítems con estado de disponibilidad."""
        print(f"| {'Item ID':10} | {'Title':38} | {'Author':30} | {'Status':10} |")
        print("-" * 100)
        for item in items:
            status = "Borrowed" if not item.is_available() else "Available"
            print(f"| {item.id:10} | {item.title:38} | {item.author:30} | {status:10} |")
        print("-" * 100)

    @staticmethod
    def print_grouped_by_date(grouped: dict) -> None:
        """Imprime ítems agrupados por su fecha de vencimiento."""
        for date, items in grouped.items():
            print(f"\nDue Date: {date}")
            print(f"| {'Item ID':10} | {'Title':40} | {'Author':30} |")
            print("-" * 90)
            for item in items:
                print(f"| {item.id:10} | {item.title:40} | {item.author:30} |")
            print("-" * 90)

    @staticmethod
    def print_success(msg: str) -> None:
        """Muestra un mensaje de éxito."""
        print(f"\n>>> SUCCESS: {msg}")

    @staticmethod
    def print_error(msg: str) -> None:
        """Muestra un mensaje de error."""
        print(f"\n!!! ERROR: {msg}")



##---------------------------------------------------------------------------------
##EN CASO SE DESEE PROBAR O COMO LLAMAR A LAS FUNCIONES

"""

# --- ZONA DE PRUEBAS (Copia esto al final de tu archivo display.py) ---

if __name__ == "__main__":
    print("--- INICIO DE PRUEBAS DE DISPLAY ---\n")

    # 1. Probar Header
    # Función: Display.print_header()
    # Data: Un string con el título
    Display.print_header("Pantalla Principal de la Biblioteca")

    # 2. Probar Menú
    # Función: Display.print_menu()
    # Data: Título (str) y una lista de opciones (list[str])
    opciones = ["Gestionar Miembros", "Gestionar Ítems", "Reportes"]
    Display.print_menu("Menú Principal", opciones)

    # 3. Probar Tabla de Miembros
    # Función: Display.print_members_table()
    # Data: Una lista. El código soporta diccionarios o objetos. Usaremos diccionarios simples para no depender de otra clase.
    print("\n--- Tabla de Miembros ---")
    miembros_falsos = [
        {
            "id": 101, 
            "name": "Juan Pérez", 
            "email": "juan@email.com", 
            "phone": "555-1234", 
            "birthdate": "1990-05-20"
        },
        {
            "id": 102, 
            "name": "Maria Gomez", 
            "email": "maria@email.com", 
            "phone": "555-5678", 
            "birthdate": "1985-11-10"
        }
    ]
    Display.print_members_table(miembros_falsos)

    # 4. Probar Tabla de Ítems
    # Función: Display.print_items_table()
    # Data: Lista de objetos. Como el método llama a .is_available(), necesitamos crear una clase mini para simularlo.
    
    # Definimos una clase temporal solo para la prueba (Mock)
    class MockItem:
        def __init__(self, iid, title, author, is_avail):
            self.id = iid
            self.title = title
            self.author = author
            self._avail = is_avail
        def is_available(self):
            return self._avail

    items_falsos = [
        MockItem(1, "El Principito", "Saint-Exupéry", True),  # Disponible
        MockItem(2, "1984", "Orwell", False),                 # Prestado
        MockItem(3, "Dune", "Herbert", True)                  # Disponible
    ]
    print("\n--- Tabla de Ítems ---")
    Display.print_items_table(items_falsos)

    # 5. Probar Agrupados por Fecha
    # Función: Display.print_grouped_by_date()
    # Data: Un diccionario { fecha_str: lista_de_items }
    print("\n--- Ítems Agrupados por Vencimiento ---")
    agrupados_falsos = {
        "2023-12-01": [items_falsos[1]], # El libro 1984
        "2023-12-05": [items_falsos[0], items_falsos[2]]
    }
    Display.print_grouped_by_date(agrupados_falsos)

    # 6. Probar Mensajes
    # Función: Display.print_success() y Display.print_error()
    print("\n--- Mensajes de Sistema ---")
    Display.print_success("El miembro fue registrado correctamente.")
    Display.print_error("No se encontró el ID del ítem.")

"""

    print("\n--- FIN DE PRUEBAS ---")
