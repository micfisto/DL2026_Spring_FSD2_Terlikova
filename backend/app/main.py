from fastapi import FastAPI
from sqlalchemy import text
from db import engine, Base

app = FastAPI(
    title="Geo Quiz API",
    description="Backend для географической викторины",
    version="1.0.0"
)


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
