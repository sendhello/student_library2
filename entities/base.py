from abc import ABC, abstractmethod
from typing import Self


class BaseEntity(ABC):
    """
    Abstract base class for library entities.

    Subclasses must implement to_dict() and from_dict().
    """

    def __init__(self, _id: int):
        self._id = _id

    @property
    def id(self) -> int:
        """Read-only entity ID."""
        
        return self._id

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialise the entity to a plain dictionary for JSON storage."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> Self:
        """Deserialise an entity from a dictionary (loaded from JSON)."""
        ...

    def __eq__(self, other: object) -> bool:
        """Two entities are equal if they share the same type and ID."""
        
        if not isinstance(other, self.__class__):
            return NotImplemented
        
        return self._id == other._id

    def __hash__(self) -> int:
        """Allow entities to be used in sets and as dict keys."""
        
        return hash((self.__class__.__name__, self._id))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id})"
