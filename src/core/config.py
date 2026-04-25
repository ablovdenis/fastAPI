from pydantic import SecretStr
from pydantic_settings import BaseSettings


# class Settings(BaseSettings):
#     ORIGINS: str
#     PORT: int = 8000
#     ROOT_PATH: str = ''

#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
#     SECRET_AUTH_KEY: SecretStr
#     AUTH_ALGORITHM: str = "HS256"

#     SQLITE_URL: str

class Settings:
    PORT: int = 8000
    ROOT_PATH: str = ''

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    SECRET_AUTH_KEY: SecretStr = SecretStr("Kak_je_mena_eto_zadolbalo,_#$%...")
    AUTH_ALGORITHM: str = "HS256"

    SQLITE_URL: str

settings = Settings()