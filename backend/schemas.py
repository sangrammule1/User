from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str