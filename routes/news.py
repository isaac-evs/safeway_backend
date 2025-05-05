from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import user, news
from controllers import users, news
import database
from routes.auth import get_current_user

router = APIRouter(prefix="/news", tags=["news"])

@router.post("/", response_model=news.NewsOut)
def create(news: news.NewsCreate, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    return news.create_news(db, news, user.name)

@router.get("/", response_model=List[news.NewsOut])
def read_all(db: Session = Depends(database.get_db)):
    return news.get_news(db)

@router.get("/by_source/{source}", response_model=List[news.NewsOut])
def read_by_source(source: str, db: Session = Depends(database.get_db)):
    return news.get_news_by_source(db, source)

@router.get("/{news_id}", response_model=news.NewsOut)
def read_one(news_id: int, db: Session = Depends(database.get_db)):
    news = news.get_news_by_id(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@router.put("/{news_id}", response_model=news.NewsOut)
def update(news_id: int, news: news.NewsCreate, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    return news.update_news(db, news_id, news, user.name)

@router.delete("/{news_id}")
def delete(news_id: int, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    news.delete_news(db, news_id, user.name)
    return {"message": "Deleted"}