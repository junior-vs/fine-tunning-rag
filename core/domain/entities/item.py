"""Item domain entity."""
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Item:
    """Item entity representing a domain object."""

    id: UUID
    name: str
    description: str | None = None

    @classmethod
    def create(cls, name: str, description: str | None = None) -> "Item":
        """Factory method to create a new Item with generated ID."""
        return cls(id=uuid4(), name=name, description=description)
