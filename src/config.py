from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    host: str
    port: int = 5432
    user: str
    password: SecretStr
    db: str

    @property
    def database_url(self):
        """Для FastAPI (асинхронно)"""
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"

    @property
    def migration_url(self):
        return f"postgresql://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        extra="ignore",
    )


class OmdbSettings(BaseSettings):
    api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="OMDB_",
        extra="ignore",
    )


class AppSettings(BaseSettings):
    debug: bool = False
    port: int = 8000


    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="APP_", extra="ignore"
    )

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        extra="ignore",
    )


class Settings(BaseSettings):
    postgres_settings: PostgresSettings = PostgresSettings()
    app_settings: AppSettings = AppSettings()
    omdb: OmdbSettings = OmdbSettings()

settings = Settings()
