from fastapi import FastAPI
from routes import auth, news
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://safestway.click", "https://www.safestway.click"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Safeway API is running"}

app.include_router(auth.router)
app.include_router(news.router)
