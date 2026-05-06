from app.config import settings
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openrouter import OpenRouterProvider


openrouter_provider = OpenRouterProvider(api_key=settings.ai_api_key)

model = OpenRouterModel(
    model_name="google/gemma-4-31b-it:free",
    provider=openrouter_provider
)
