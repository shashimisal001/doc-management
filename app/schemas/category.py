from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]

    class Config:
        from_attributes = True