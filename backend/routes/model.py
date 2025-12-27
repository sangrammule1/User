```python
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

# Assume you have a database setup with a SQLAlchemy session
# and a Model called Entity

# Replace with your actual database setup and model
class Entity(BaseModel):
    id: Optional[int] = None
    field1: str
    field2: int


router = APIRouter(prefix="/entity", tags=["Entity"])


# Dummy database for demonstration purposes.  Replace with a real database.
db = []


@router.post("/", response_model=Entity, status_code=status.HTTP_201_CREATED)
async def create_entity(entity: Entity):
    """
    Create a new entity.
    """
    entity.id = len(db) + 1  # Assign a unique ID
    db.append(entity)
    return entity


@router.get("/", response_model=List[Entity], status_code=status.HTTP_200_OK)
async def read_entities():
    """
    Read all entities.
    """
    return db


@router.get("/{entity_id}", response_model=Entity, status_code=status.HTTP_200_OK)
async def read_entity(entity_id: int):
    """
    Read a single entity by ID.
    """
    for entity in db:
        if entity.id == entity_id:
            return entity
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")


@router.put("/{entity_id}", response_model=Entity, status_code=status.HTTP_200_OK)
async def update_entity(entity_id: int, entity: Entity):
    """
    Update an existing entity.
    """
    for i, existing_entity in enumerate(db):
        if existing_entity.id == entity_id:
            entity.id = entity_id  # Keep the original ID
            db[i] = entity
            return entity
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity(entity_id: int):
    """
    Delete an entity by ID.
    """
    for i, entity in enumerate(db):
        if entity.id == entity_id:
            del db[i]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
```