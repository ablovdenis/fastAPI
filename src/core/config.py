from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ORIGINS: str = ''
    PORT: int = 8000
    ROOT_PATH: str = ''

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 8
    SECRET_AUTH_KEY: SecretStr = SecretStr('')
    AUTH_ALGORITHM: str = "HS256"

    POSTGRES_SCHEMA: str = ''
    POSTGRES_HOST: str = ''
    POSTGRES_DB: str = ''
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: SecretStr = SecretStr('')
    POSTGRES_PASSWORD: SecretStr = SecretStr('')
    POSTGRES_RECONNECT_INTERVAL_SEC: int = 1

    @property
    def postgres_url(self) -> str:
        creds = f"{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}"
        return f"postgresql+asyncpg://{creds}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()