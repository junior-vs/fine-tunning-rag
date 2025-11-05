"""Unit tests for use cases."""
from unittest.mock import Mock
from uuid import uuid4

from core.application.use_cases.create_item_uc import CreateItemUseCase
from core.domain.entities.item import Item
from core.domain.repositories.item_repo import AbstractItemRepository


def test_create_item_use_case() -> None:
    """Test CreateItemUseCase with a mocked repository."""
    mock_repo = Mock(spec=AbstractItemRepository)

    item_id = uuid4()
    expected_item = Item(id=item_id, name="Test Item", description="Test Description")
    mock_repo.save.return_value = expected_item

    use_case = CreateItemUseCase(repository=mock_repo)
    result = use_case.execute(name="Test Item", description="Test Description")

    mock_repo.save.assert_called_once()
    assert result.name == "Test Item"
    assert result.description == "Test Description"


def test_create_item_use_case_without_description() -> None:
    """Test CreateItemUseCase without description."""
    mock_repo = Mock(spec=AbstractItemRepository)

    item_id = uuid4()
    expected_item = Item(id=item_id, name="Test Item", description=None)
    mock_repo.save.return_value = expected_item

    use_case = CreateItemUseCase(repository=mock_repo)
    result = use_case.execute(name="Test Item")

    mock_repo.save.assert_called_once()
    assert result.name == "Test Item"
    assert result.description is None
