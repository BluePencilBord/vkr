from fastapi import FastAPI


app = FastAPI(
    title = "GDD analysis API",
    description = "Бэк для мультиагентной системы анализа GDD"
)

@app.get("/")
async def root():
    return {"message": "Все работает"}
