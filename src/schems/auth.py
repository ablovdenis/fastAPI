from pydantic import Field, BaseModel


class Token(BaseModel):
    access_token: str = Field(description="Токен доступа к системе.")
    token_type: str = Field(description="Тип токена.")