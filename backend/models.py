from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(255))


```python
from sqlalchemy import Integer, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class model(Base):
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True)
```