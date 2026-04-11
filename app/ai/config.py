from app.config import settings
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

google_provider = GoogleProvider(api_key=settings.gemini_api_key)

flash_model = GoogleModel(model_name="gemini-2.5-flash-lite", provider=google_provider)
pro_model = GoogleModel(model_name="gemini-2.5-flash-lite", provider=google_provider)
