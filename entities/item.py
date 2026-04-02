"""Item class for representing library items."""
# item.py

class Item:
    """
    Representa un recurso de la biblioteca.
    Maneja el estado de préstamo y la conversión a diccionarios para persistencia.
    """
    def __init__(self, id: int, title: str, author: str):
        """Inicializa un ítem con ID, título y autor."""
        self.id = id
        self.title = title
        self.author = author
        self.borrowed_by = None  # Almacena el ID del miembro (int)
        self.due_date = None     # Formato 'YYYY-MM-DD' (str)

    def borrow(self, member_id: int, due_date: str) -> bool:
        """Asigna el ítem a un miembro y establece la fecha de vencimiento."""
        if self.is_available():
            self.borrowed_by = member_id
            self.due_date = due_date
            return True
        return False

    def return_item(self) -> bool:
        """Restablece el estado del ítem a disponible."""
        if not self.is_available():
            self.borrowed_by = None
            self.due_date = None
            return True
        return False

    def is_available(self) -> bool:
        """Verifica si el ítem no está prestado actualmente."""
        return self.borrowed_by is None

    def to_dict(self) -> dict:
        """Convierte la instancia en un diccionario para guardar en JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "borrowed_by": self.borrowed_by,
            "due_date": self.due_date
        }

    @staticmethod
    def from_dict(data: dict):
        """Crea un objeto Item a partir de un diccionario de datos."""
        item = Item(data['id'], data['title'], data['author'])
        item.borrowed_by = data.get('borrowed_by')
        item.due_date = data.get('due_date')
        return item

    def __str__(self):
        return f"Item ID: {self.id} | Title: {self.title} | Author: {self.author}"

    def __repr__(self):
        return self.__str__()


