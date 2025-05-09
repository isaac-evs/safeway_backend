from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, date
from shapely import wkb
from shapely.geometry import Point
from typing import Optional
from datetime import datetime

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
    coordinates: Optional[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.coordinates:
            geom = wkb.loads(self.coordinates.data)
            self.coordinates = geom.wkt

    class Config:
        orm_mode = True
