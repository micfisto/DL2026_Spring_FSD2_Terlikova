from fastapi import FastAPI

from .middleware.cors import setup_cors
from .routes import game_router
from .routes.leaderboard import router as leaderboard_router
from .routes.admin import router as admin_router

app = FastAPI(
    title="GeoQuiz API",
    description="Backend для географической викторины",
)

setup_cors(app)

app.include_router(game_router)
app.include_router(leaderboard_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {"message": "Geo Quiz API is running"}