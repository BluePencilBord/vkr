from fastapi import FastAPI
from app.api import users
from app.config import settings


app = FastAPI(
    title = settings.project_name,
    version = settings.version,
    description = "Бэк для мультиагентной системы анализа GDD"
)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Все работает"}
