from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session
from vender_api.models import User
from vender_api.schemas.auth_schemas import Token
from vender_api.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2Form, session: Session):
    """
    Autentica o usuário e retorna um token de acesso.
    Essa rota é utilizada para realizar o login do usuário, recebendo email e senha e retornando um token JWT para autenticação nas próximas requisições.

    Parâmetros:
        - form_data: Dados do formulário OAuth2 (username = email, password = senha).

    Retorna:
        Um dicionário contendo o access_token (JWT) e o token_type (sempre 'bearer').

    Erros:
        - 401: Email ou senha incorretos.
    """
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
async def refresh_token(user: CurrentUser):
    """
    Gera um novo token de acesso para o usuário autenticado.
    Essa rota é utilizada para renovar o token JWT de um usuário já autenticado, sem necessidade de informar email e senha novamente.

    Parâmetros:
        - user: Usuário autenticado (obtido automaticamente pelo sistema).

    Retorna:
        Um novo access_token (JWT) e o token_type (sempre 'bearer').
    """
    new_access_token = create_access_token(data={'sub': user.email})
    return {'access_token': new_access_token, 'token_type': 'bearer'}
