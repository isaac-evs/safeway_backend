from sqlalchemy import Column, Integer, String, Text, DateTime, Date, CheckConstraint, func, UniqueConstraint
from geoalchemy2 import Geography
from database import Base
from geoalchemy2.shape import to_shape
from sqlalchemy.ext.hybrid import hybrid_property

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    news_source = Column(Text)
    title = Column(Text)
    description = Column(Text)
    coordinates = Column(Geography)
    type = Column(Text, CheckConstraint("type IN ('crime', 'infrastructure', 'hazard', 'social')"))
    date = Column(Date)
    url = Column(Text, unique=True)
    processed_at = Column(DateTime, server_default=func.now())

    @hybrid_property
    def coordinates_str(self):
        if self.coordinates:
            return to_shape(self.coordinates).wkt
        return None