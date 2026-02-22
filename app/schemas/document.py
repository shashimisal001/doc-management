from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DocumentListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    filename: str
    category_id: Optional[int]
    category_name: Optional[str]
    uploaded_at: datetime

    class Config:
        from_attributes = True