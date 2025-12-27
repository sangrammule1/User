```python
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param import Body
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal

router = APIRouter(prefix="/entity", tags=["Entity"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Entity, status_code=status.HTTP_201_CREATED)
async def create_entity(entity: schemas.EntityCreate, db: Session = Depends(get_db)):
    """
    Creates a new entity.
    """
    db_entity = models.Entity(**entity.dict())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity


@router.get("/", response_model=List[schemas.Entity])
async def read_entities(db: Session = Depends(get_db)):
    """
    Retrieves all entities.
    """
    entities = db.query(models.Entity).all()
    return entities


@router.get("/{id}", response_model=schemas.Entity)
async def read_entity(id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single entity by ID.
    """
    entity = db.query(models.Entity).filter(models.Entity.id == id).first()
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
    return entity


@router.put("/{id}", response_model=schemas.Entity)
async def update_entity(id: int, entity: schemas.EntityUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing entity by ID.
    """
    db_entity = db.query(models.Entity).filter(models.Entity.id == id).first()
    if db_entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")

    for field, value in entity.dict(exclude_unset=True).items():
        setattr(db_entity, field, value)

    db.commit()
    db.refresh(db_entity)
    return db_entity


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity(id: int, db: Session = Depends(get_db)):
    """
    Deletes an entity by ID.
    """
    db_entity = db.query(models.Entity).filter(models.Entity.id == id).first()
    if db_entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
    db.delete(db_entity)
    db.commit()
    return
```