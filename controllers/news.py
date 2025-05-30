from sqlalchemy.orm import Session
from models import news as news_model, users
from schemas import news, user
from utils.auth import get_password_hash
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from geoalchemy2.shape import to_shape

def create_news(db: Session, news: news.NewsCreate, username: str):
    db_news = news_model.News(**news.model_dump(), news_source=username)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    db_news.coordinates = db_news.coordinates_str
    return db_news

def get_news(db: Session):
    news = db.query(news_model.News).all()
    for n in news:
        n.coordinates = to_shape(n.coordinates).wkt if n.coordinates else None
    return news

def get_news_by_id(db: Session, news_id: int):
    news = db.query(news_model.News).filter(news_model.News.id == news_id).first()
    if news:
        news.coordinates = to_shape(news.coordinates).wkt if news.coordinates else None
    return news

def get_news_by_source(db: Session, source: str):
    news = db.query(news_model.News).filter(news_model.News.news_source == source).all()
    for n in news:
        n.coordinates = to_shape(n.coordinates).wkt if n.coordinates else None
    return news

def update_news(db: Session, news_id: int, news: news.NewsCreate, username: str):
    db_news = get_news_by_id(db, news_id)
    if db_news and db_news.news_source == username:
        for field, value in news.model_dump().items():
            setattr(db_news, field, value)
        db.commit()
        db.refresh(db_news)
        return db_news
    raise HTTPException(status_code=403, detail="Not authorized")

def delete_news(db: Session, news_id: int, username: str):
    db_news = get_news_by_id(db, news_id)
    if db_news and db_news.news_source == username:
        db.delete(db_news)
        db.commit()
        return db_news
    raise HTTPException(status_code=403, detail="Not authorized")