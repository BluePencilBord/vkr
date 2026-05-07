from app.config import settings
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openrouter import OpenRouterProvider


openrouter_provider = OpenRouterProvider(api_key=settings.ai_api_key)

model = OpenRouterModel(
    model_name="google/gemma-4-26b-a4b-it",
    provider=openrouter_provider,
)
