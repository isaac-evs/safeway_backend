from sqlalchemy.orm import Session
from models import users, news
from schemas import user
from utils.auth import get_password_hash
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def get_user_by_email(db: Session, email: str):
    return db.query(users.User).filter(users.User.email == email).first()

def get_user_by_name(db: Session, name: str):
    return db.query(users.User).filter(users.User.name == name).first()

def check_name_conflict_with_news(db: Session, name: str):
    return db.query(news.News).filter(news.News.news_source == name).first() is not None

def create_user(db: Session, user: user.UserCreate):
    if get_user_by_name(db, user.name) or check_name_conflict_with_news(db, user.name):
        raise HTTPException(status_code=400, detail="Name already taken or conflicts with existing news source")
    hashed_password = get_password_hash(user.password)
    db_user = users.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user