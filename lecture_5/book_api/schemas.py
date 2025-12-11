from pydantic import BaseModel, ConfigDict
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    year: Optional[int] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int]

    model_config = ConfigDict(from_attributes=True)
