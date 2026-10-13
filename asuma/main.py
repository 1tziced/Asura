"""Asuma — только интерфейс. Запуск:  python main.py  →  http://127.0.0.1:8000"""
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import init_db

BASE_DIR = Path(__file__).parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # создаёт таблицы, если их ещё нет
    yield


app = FastAPI(title="Asuma", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Демо-данные для оформления. Потом заменятся запросами к БД.
DEMO_TRACKS = [
    dict(id=1, title="Полночный маршрут", artist="Лиса и Радио", album="Окна", duration="3:42", plays=18420, hue=160)
]


def page(request: Request, name: str, active: str, **extra):
    ctx = {"tracks": DEMO_TRACKS, "user": None, "active": active, **extra}
    return templates.TemplateResponse(request, name, ctx)


@app.get("/")
async def index(request: Request):
    return page(request, "index.html", "home")


@app.get("/search")
async def search(request: Request):
    return page(request, "search.html", "search")


@app.get("/favorites")
async def favorites(request: Request):
    return page(request, "favorites.html", "favorites")


@app.get("/playlists")
async def playlists(request: Request):
    return page(request, "playlists.html", "playlists")


@app.get("/history")
async def history(request: Request):
    return page(request, "history.html", "history")


@app.get("/login")
async def login(request: Request):
    return page(request, "auth.html", "", mode="login")


@app.get("/register")
async def register(request: Request):
    return page(request, "auth.html", "", mode="register")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
