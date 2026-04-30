from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str = "GDD Analysis API"
    version: str = "0.1.0"
    
    database_url: str

    s3_access_key: str
    s3_secret_key: str
    s3_bucket_name: str
    s3_endpoint_url: str = "https://storage.yandexcloud.net"

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    rabbitmq_url: str

    ai_api_key: str

    model_config = SettingsConfigDict(env_file = ".env", env_file_encoding = "utf-8", extra="ignore")

settings = Settings()