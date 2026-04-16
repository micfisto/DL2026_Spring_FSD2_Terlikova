from fastapi import FastAPI
from sqlalchemy import text
from .db import engine, Base

from fastapi.middleware.cors import CORSMiddleware
from .routes import game_router
from .routes.leaderboard import router as leaderboard_router
from .routes.admin import router as admin_router

app = FastAPI(
    title="GeoQuiz API",
    description="Backend для географической викторины",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(game_router)
app.include_router(leaderboard_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {"message": "Geo Quiz API is running"}