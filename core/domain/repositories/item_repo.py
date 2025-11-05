"""Abstract repository interface for Item entity."""
from abc import ABC, abstractmethod
from uuid import UUID

from core.domain.entities.item import Item


class AbstractItemRepository(ABC):
    """Abstract repository defining the contract for Item persistence."""

    @abstractmethod
    def save(self, item: Item) -> Item:
        """Save an item and return the saved instance."""
        pass

    @abstractmethod
    def find_by_id(self, item_id: UUID) -> Item | None:
        """Find an item by its ID."""
        pass

    @abstractmethod
    def find_all(self) -> list[Item]:
        """Retrieve all items."""
        pass

    @abstractmethod
    def delete(self, item_id: UUID) -> bool:
        """Delete an item by its ID. Returns True if deleted, False if not found."""
        pass
