from pydantic import Field, BaseModel


class Token(BaseModel):
    access_token: str = Field(description="Токен доступа к системе.")
    refresh_token: str = Field(description="Рефреш-токен.")
    token_type: str = Field(description="Тип токена.")
