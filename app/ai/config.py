from app.config import settings
from pydantic_ai.models.google import GoogleModel

flash_model = GoogleModel("gemini-2.5-flash", api_key=settings.gemini_api_key)
pro_model = GoogleModel("gemini-2.5-pro", api_key=settings.gemini_api_key)
