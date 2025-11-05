"""In-memory implementation of Item repository."""
from uuid import UUID

from core.domain.entities.item import Item
from core.domain.repositories.item_repo import AbstractItemRepository


class InMemoryItemRepository(AbstractItemRepository):
    """In-memory implementation of the Item repository."""

    def __init__(self) -> None:
        self._items: dict[UUID, Item] = {}

    def save(self, item: Item) -> Item:
        """Save an item in memory."""
        self._items[item.id] = item
        return item

    def find_by_id(self, item_id: UUID) -> Item | None:
        """Find an item by its ID."""
        return self._items.get(item_id)

    def find_all(self) -> list[Item]:
        """Retrieve all items."""
        return list(self._items.values())

    def delete(self, item_id: UUID) -> bool:
        """Delete an item by its ID."""
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False
