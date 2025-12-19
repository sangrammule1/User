from pydantic import BaseModel, {name}
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str