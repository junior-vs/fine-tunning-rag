"""HTTP API application using FastAPI."""
from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core.application.use_cases.create_item_uc import CreateItemUseCase
from core.infrastructure.repositories.in_memory_item_repo import InMemoryItemRepository

app = FastAPI(title="Item Management API", version="1.0.0")

repository = InMemoryItemRepository()


class CreateItemRequest(BaseModel):
    """Request model for creating an item."""
    name: str
    description: str | None = None


class ItemResponse(BaseModel):
    """Response model for an item."""
    id: UUID
    name: str
    description: str | None = None


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(request: CreateItemRequest) -> ItemResponse:
    """Create a new item."""
    use_case = CreateItemUseCase(repository)
    item = use_case.execute(name=request.name, description=request.description)

    return ItemResponse(
        id=item.id,
        name=item.name,
        description=item.description
    )


@app.get("/items", response_model=list[ItemResponse])
def list_items() -> list[ItemResponse]:
    """List all items."""
    items = repository.find_all()
    return [
        ItemResponse(id=item.id, name=item.name, description=item.description)
        for item in items
    ]


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: UUID) -> ItemResponse:
    """Get an item by ID."""
    item = repository.find_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return ItemResponse(
        id=item.id,
        name=item.name,
        description=item.description
    )


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: UUID) -> None:
    """Delete an item by ID."""
    deleted = repository.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
