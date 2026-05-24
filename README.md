# Как поднять 

docker compose up -d

uvicorn app.main:app --reload 

faststream run app.worker:app  

npm run dev

# Создание миграции

alembic revision --autogenerate -m "Название_миграции"

alembic upgrade head