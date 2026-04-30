from app.config import settings
from pydantic_ai.models.openrouter import OpenRouterModel

model = OpenRouterModel(
    model_name="google/gemma-4-31b-it:free",
    api_key=settings.ai_api_key,
)
