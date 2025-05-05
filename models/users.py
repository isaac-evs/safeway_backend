from sqlalchemy import Column, Integer, String, Text, DateTime, Date, CheckConstraint, func, UniqueConstraint
from geoalchemy2 import Geography
from database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("name", name="uq_user_name"),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)