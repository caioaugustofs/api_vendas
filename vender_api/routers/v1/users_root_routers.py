from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session
from vender_api.models import User
from vender_api.schemas.users_schemas import (
    UserCreate,
    UserIsSuperuserUpdate,
    userPublic,
)
from vender_api.security import get_current_user, get_password_hash
from vender_api.tools.decorador import commit_and_refresh

# Rotas para gerenciamento de usuários root (superusuários).
# Permite criar o primeiro superusuário, listar, buscar por ID e alterar permissões de root.
router = APIRouter(prefix='/users_root', tags=['Users root'])


Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=userPublic,
    summary='Cria um novo usuário root',
)
@commit_and_refresh(
    status_code=400,
    detail='Erro ao criar o usuário root',
)
async def create_user_root(user: UserCreate, session: Session):
    """
    Cria o primeiro usuário root (superusuário) do sistema.

    Parâmetros:
        - user: Dados do novo usuário (nome, email, senha).

    Retorna:
        Usuário root criado (dados públicos).

    Erros:
        - 400: Já existe um superusuário cadastrado ou usuário já existe.
    """
    # funcao funciona para criar o primeiro  superuser   ele so funciona um vez
    # se existir um usuario superuser ele vai não criar um usuario

    db_superuser = await session.scalar(select(User).where(User.is_superuser))

    if db_superuser:
        raise HTTPException(
            status_code=400,
            detail='Internal server error',
        )

    # Verifica se o usuario ja existe
    db_user_root = await session.scalar(
        select(User).where(
            or_(
                User.username == user.username,
                User.email == user.email,
            )
        )
    )

    if db_user_root:
        raise HTTPException(
            status_code=400,
            detail='User already exists',
        )

    try:
        hashed_password = get_password_hash(user.password)

        new_user_root = User(
            username=user.username,
            email=user.email,
            password=hashed_password,
            is_superuser=True,
            is_verified=True,
            is_active=True,
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail='Error creating user',
        )

    session.add(new_user_root)
    return new_user_root


@router.get(
    '/',
    response_model=list[userPublic],
    status_code=HTTPStatus.OK,
    summary='Retorna todos os usuários root',
)
async def get_users_root(
    session: Session,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 25,
):
    """
    Lista todos os usuários root (superusuários) cadastrados.

    Parâmetros:
        - current_user: Usuário autenticado (precisa ser superusuário).
        - skip: Quantidade de registros a pular (paginação).
        - limit: Quantidade máxima de registros a retornar.

    Retorna:
        Lista de usuários root (dados públicos).

    Erros:
        - 403: Não autorizado (usuário não é superusuário).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail='Not authorized to perform this action'
        )

    db_users = await session.execute(select(User).offset(skip).limit(limit))
    return db_users.scalars().all()


@router.get(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    summary='Retorna um usuário root pelo ID',
)
async def get_user_by_user_root(
    user_id: int, session: Session, current_user: CurrentUser
):
    """
    Busca um usuário root (superusuário) pelo ID.

    Parâmetros:
        - user_id: ID do usuário.
        - current_user: Usuário autenticado (precisa ser superusuário).

    Retorna:
        Usuário encontrado (dados públicos).

    Erros:
        - 403: Não autorizado (usuário não é superusuário).
        - 404: Usuário não encontrado.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail='Not authorized to perform this action'
        )

    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )

    return db_user


@router.patch(
    '/{user_id}/is_superuser',
    response_model=userPublic,
    summary='Consede  ou remove a permissao de root',
)
@commit_and_refresh(
    status_code=400,
    detail='Erro ao atualizar o usuário',
)
async def update_user_is_superuser(
    user_id: int,
    is_superuser_update: UserIsSuperuserUpdate,
    session: Session,
    current_user: CurrentUser,
):
    """
    Concede ou remove a permissão de superusuário (root) de um usuário pelo ID.

    Parâmetros:
        - user_id: ID do usuário.
        - is_superuser_update: Novo status de superusuário (True ou False).
        - current_user: Usuário autenticado (precisa ser superusuário).

    Retorna:
        Usuário atualizado (dados públicos).

    Erros:
        - 403: Não autorizado (usuário não é superusuário).
        - 404: Usuário não encontrado.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail='Not authorized to perform this action'
        )

    db_user = await session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    db_user.is_superuser = is_superuser_update.is_superuser
    return db_user
