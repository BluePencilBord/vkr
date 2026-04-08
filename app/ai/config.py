from app.config import settings


def get_llm_config(temperature: float = 0.2) -> dict:
    return {
        "config_list": [
            {
                "model": "gemini-2.5-flash",
                "api_key": settings.gemini_api_key,
                "api_type": "google"
            }
        ],
        "temperature": temperature
    }