from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_PORT: int = 6379
    REDIS_HOST: str = "localhost"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        # env_file_encoding= "utf-8",
    )


Config = Settings()
