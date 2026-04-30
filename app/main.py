from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import users, projects
from app.config import settings
from app.worker import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.connect()
    yield
    await broker.stop()


app = FastAPI(
    title = settings.project_name,
    version = settings.version,
    description = "Бэк для мультиагентной системы анализа GDD",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(projects.router)


@app.get("/")
async def root():
    return {"message": "Все работает"}
