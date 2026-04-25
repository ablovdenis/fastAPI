from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.database import get_db
from src.schems.auth import Token
from src.domain.auth.use_cases.auth_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.core.exceptions.domain_exceptions import WrongUserPasswordException, UserNotFoundByNicknameException
from src.api.depends import create_access_token_use_case, auth_user_use_case

router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_use_case: AuthenticateUserUseCase = Depends(auth_user_use_case),
    create_token_use_case: CreateAccessTokenUseCase = Depends(create_access_token_use_case),
    DataBase: Session = Depends(get_db)
) -> Token:
    try:
        user = auth_use_case.get_detail(DataBase, form_data.username, form_data.password)
    except WrongUserPasswordException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.get_detail(),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserNotFoundByNicknameException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())

    access_token = create_token_use_case.create_token(user.nickname)

    return Token(access_token=access_token, token_type="bearer")