from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, date

class NewsBase(BaseModel):
    title: str
    description: Optional[str]
    coordinates: Optional[str]
    type: str
    date: date
    url: str

class NewsCreate(NewsBase):
    pass

class NewsOut(NewsBase):
    id: int
    news_source: str
    processed_at: datetime

    class Config:
        orm_mode = True
