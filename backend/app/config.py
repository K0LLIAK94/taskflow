from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/taskflow"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 1440
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
