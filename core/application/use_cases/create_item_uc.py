"""Use case for creating a new Item."""
from core.domain.entities.item import Item
from core.domain.repositories.item_repo import AbstractItemRepository


class CreateItemUseCase:
    """Use case to create and save a new Item."""

    def __init__(self, repository: AbstractItemRepository) -> None:
        """Initialize with repository dependency (Dependency Inversion)."""
        self._repository = repository

    def execute(self, name: str, description: str | None = None) -> Item:
        """Execute the use case to create a new item."""
        item = Item.create(name=name, description=description)
        return self._repository.save(item)
