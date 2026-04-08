from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    flight_events_api_url: str = "http://localhost:8001"
    log_level: str = "INFO"
    log_format: str = "text"  # "text" en dev | "json" en prod

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()