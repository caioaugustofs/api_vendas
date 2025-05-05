# Rotas de usuários
# Este módulo contém as rotas relacionadas à manipulação de usuários na API.
# Todas as rotas estão documentadas em português para facilitar o entendimento.

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import not_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session
from vender_api.models import User
from vender_api.schemas.users_schemas import (
    UserCreate,
    UserIsActiveUpdate,
    UserIsVerifiedUpdate,
    UserPasswordUpdate,
    UserUpdate,
    userPublic,
)
from vender_api.security import get_current_user, get_password_hash
from vender_api.tools.decorador import commit_and_refresh

router = APIRouter(prefix='/users', tags=['Users'])


# Dependências
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get(
    '/',
    response_model=list[userPublic],
    status_code=HTTPStatus.OK,
    summary='Retorna todos os usuários',
)
async def get_users(
    session: Session,
    skip: int = 0,
    limit: int = 25,
):
    """
    Retorna todos os usuários cadastrados, exceto os superusuários.

    Parâmetros:
        - skip: Número de usuários a pular (paginação).
        - limit: Número máximo de usuários a retornar.

    Retorna:
        Lista de usuários públicos (sem informações sensíveis).
    """
    db_users = await session.execute(
        select(User).where(not_(User.is_superuser)).offset(skip).limit(limit)
    )
    return db_users.scalars().all()


@router.get(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    summary='Retorna um usuário pelo ID',
)
async def get_user_by_user(user_id: int, session: Session):
    """
    Retorna um usuário específico pelo seu ID.
    Essa rota é útil para obter informações detalhadas sobre um usuário específico.

    Parâmetros:
        - user_id: ID do usuário a ser buscado.

    Retorna:
        Usuário correspondente ao ID informado.

    Erros:
        - 404: Usuário não encontrado.
    """
    db_user = await session.scalar(
        select(User).where(or_(User.id == user_id, not_(User.is_superuser)))
    )
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    return db_user


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=userPublic,
    summary='Cria um novo usuário',
)
@commit_and_refresh(status_code=400, detail='Erro ao criar usuário')
async def create_user(user: UserCreate, session: Session):
    """
    Cria um novo usuário no sistema, armazenando suas informações de forma segura.

    Parâmetros:
        - user: Dados do novo usuário (username, email, senha).

    Retorna:
        Usuário criado (dados públicos).

    Erros:
        - 400: Usuário já existe (username ou email duplicado).
    """
    db_user = await session.scalar(
        select(User).where(
            or_(
                User.username == user.username,
                User.email == user.email,
            )
        )
    )
    if db_user:
        raise HTTPException(
            status_code=400,
            detail='User already exists',
        )
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
    )
    session.add(new_user)
    return new_user


@router.patch(
    '/{user_id}',
    response_model=userPublic,
    status_code=HTTPStatus.OK,
    summary='Atualiza  informações do usuário',
)
@commit_and_refresh(status_code=400, detail='Erro ao atualizar usuário')
async def update_user(user_id: int, user_update: UserUpdate, session: Session):
    """
    Atualiza um ou mais campos do usuário (exceto username, email e senha),
    permitindo a atualização de informações adicionais, como nome, sobrenome, etc.
    Essa operação é útil para manter os dados do usuário atualizados.

    Parâmetros:
        - user_id: ID do usuário a ser atualizado.
        - user_update: Dados a serem atualizados (apenas campos enviados serão alterados).

    Retorna:
        Usuário atualizado (dados públicos).

    Erros:
        - 404: Usuário não encontrado.
        - 400: Nenhum campo enviado para atualizar.
    """
    db_user = await session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    update_data = user_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=400, detail='Nenhum campo enviado para atualizar.'
        )
    for field, value in update_data.items():
        setattr(db_user, field, value)
    return db_user


@router.patch(
    '/{user_id}/password',
    response_model=userPublic,
    status_code=HTTPStatus.OK,
    summary='Atualiza a senha do usuário',
)
async def update_user_password(
    user_id: int, password_update: UserPasswordUpdate, session: Session
):
    """
    Atualiza a senha de um usuário especificado pelo ID no sistema.
    Essa operação é útil para redefinir senhas ou atualizar senhas existentes.

    Parâmetros:
        - user_id: ID do usuário.
        - password_update: Nova senha.

    Retorna:
        Usuário atualizado (dados públicos).

    Erros:
        - 404: Usuário não encontrado.
        - 500: Erro ao atualizar a senha.
    """
    db_user = await session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    try:
        hashed_password = get_password_hash(password_update.password)
        db_user.password = hashed_password
        await session.commit()
        await session.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail='Erro ao atualizar a senha do usuário.',
        ) from e


# PATCH para atualizar is_active
@router.patch(
    '/{user_id}/is_active',
    response_model=userPublic,
    status_code=HTTPStatus.OK,
    summary='Atualiza o status de atividade do usuário',
)
@commit_and_refresh(
    status_code=400, detail='Erro ao atualizar status de atividade'
)
async def update_user_is_active(
    user_id: int, is_active_update: UserIsActiveUpdate, session: Session
):
    """
    Atualiza o status de atividade (is_active) de um usuário,
    permitindo ativar ou desativar o usuário no sistema.

    Parâmetros:
        - user_id: ID do usuário.
        - is_active_update: Novo status de atividade (True ou False).


    Retorna:
        Usuário atualizado (dados públicos).

    Erros:
        - 404: Usuário não encontrado.
    """
    db_user = await session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    db_user.is_active = is_active_update.is_active
    return db_user


# PATCH para atualizar is_verified
@router.patch(
    '/{user_id}/is_verified',
    response_model=userPublic,
    status_code=HTTPStatus.OK,
    summary='Atualiza o status de verificação do usuário',
)
@commit_and_refresh(
    status_code=400, detail='Erro ao atualizar status de verificação'
)
async def update_user_is_verified(
    user_id: int, is_verified_update: UserIsVerifiedUpdate, session: Session
):
    """
    Atualiza o status de verificação (is_verified) de um usuário, geralmente
    após a verificação de e-mail.

    Parâmetros:
        - user_id: ID do usuário.
        - is_verified_update: Novo status de verificação (True ou False).


    Retorna:
        Usuário atualizado (dados públicos).

    Erros:
        - 404: Usuário não encontrado.
    """
    db_user = await session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    db_user.is_verified = is_verified_update.is_verified
    return db_user


# DELETE para deletar um usuário
@router.delete(
    '/{user_id}', status_code=HTTPStatus.NO_CONTENT, summary='Deleta usuário'
)
async def delete_user(
    user_id: int, session: Session, current_user: CurrentUser
):
    """
    Deleta um usuário do sistema pelo ID.

    Parâmetros:
        - user_id: ID do usuário a ser deletado.
        - current_user: Usuário autenticado que está realizando a operação.

    Retorna:
        Nenhum conteúdo (status 204).

    Erros:
        - 404: Usuário não encontrado.
    """
    db_user = await session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    await session.delete(db_user)
    await session.commit()
