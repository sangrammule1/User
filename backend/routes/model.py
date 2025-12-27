from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Define the database base
Base = declarative_base()


# Define the Entity model
class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Added name field for example


# Define the schemas
class EntityCreate(BaseModel):
    name: str = Field(..., description="Entity name")  # Required field example


class EntityUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Entity name")


class EntityResponse(BaseModel):
    id: int
    name: str


class EntityListResponse(BaseModel):
    entities: List[EntityResponse]


# Define the database session dependency
def get_db():
    
    Dummy database session for demonstration purposes.
    Replace with your actual database connection.
    
    # In a real application, you'd use a database engine and session factory
    # For example:
    # from sqlalchemy import create_engine, Session
    # engine = create_engine("sqlite:///./test.db")  # Replace with your database URL
    # LocalSession = sessionmaker(bind=engine)
    # db = LocalSession()
    # return db
    class MockSession:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def add(self, instance):
            self.mock_data.append(instance)
        def commit(self):
            pass
        def refresh(self, instance):
            pass
        def query(self, model):
            return MockQuery(self, model)

    return MockSession()


class MockQuery:
    def __init__(self, session, model):
        self.session = session
        self.model = model
        self.results = []

    def filter(self, *args):
        return self

    def first(self):
        if self.results:
            return self.results[0]
        else:
            return None

    def all(self):
        return self.results

    def add(self, instance):
        self.session.add(instance)

    def refresh(self, instance):
        self.session.refresh(instance)

    def __iter__(self):
        return iter(self.results)


# Create the router
router = APIRouter(prefix="/entity", tags=["Entity"])


# CRUD operations

@router.post("/", response_model=EntityResponse)
async def create_entity(entity_data: EntityCreate, db: Session = Depends(get_db)):
    
    Create a new entity.
    
    new_entity = Entity(name=entity_data.name)
    db.add(new_entity)
    db.commit()
    db.refresh(new_entity)
    return EntityResponse(id=new_entity.id, name=new_entity.name)


@router.get("/", response_model=EntityListResponse)
async def read_entities(db: Session = Depends(get_db)):
    
    Read all entities.
    
    entities = db.query(Entity).all()
    return EntityListResponse(entities=[EntityResponse(id=e.id, name=e.name) for e in entities])


@router.get("/{id}", response_model=EntityResponse)
async def read_entity(id: int, db: Session = Depends(get_db)):
    
    Read a single entity by ID.
    
    entity = db.query(Entity).filter(Entity.id == id).first()
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
    return EntityResponse(id=entity.id, name=entity.name)


@router.put("/{id}", response_model=EntityResponse)
async def update_entity(id: int, entity_data: EntityUpdate, db: Session = Depends(get_db)):
    
    Update an existing entity.
    
    entity = db.query(Entity).filter(Entity.id == id).first()
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")

    if entity_data.name is not None:
        entity.name = entity_data.name

    db.commit()
    db.refresh(entity)
    return EntityResponse(id=entity.id, name=entity.name)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity(id: int, db: Session = Depends(get_db)):
    
    Delete an entity by ID.
    
    entity = db.query(Entity).filter(Entity.id == id).first()
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
    db.delete(entity)
    db.commit()