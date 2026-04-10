from fastapi import FastAPI
from sqlalchemy import text
from backend.app.db import engine, Base

from fastapi.middleware.cors import CORSMiddleware
from backend.app.models import *
from backend.app.routes import game_router
from backend.app.routes.leaderboard import router as leaderboard_router

app = FastAPI(
    title="Geo Quiz API",
    description="Backend для географической викторины",
    version="1.0.0"
)

Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(game_router)
app.include_router(leaderboard_router)

@app.get("/")
def root():
    return {"message": "Geo Quiz API is running"}


@app.get("/db-test")
def test_db():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()

            return {
                "message": "Подключение к базе успешно",
                "result": value
            }
    except Exception as e:
        return {
            "message": "Ошибка подключения к бд",
            "error": str(e)
        }