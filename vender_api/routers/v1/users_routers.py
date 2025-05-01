from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
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
):
    """Retorna todos os usuarios exceto superusers"""
    db_users = await session.execute(select(User).where(User.is_superuser == False))
    return db_users.scalars().all()


@router.get(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    summary='Retorna um usuário pelo ID',
)
async def get_user_by_user(user_id: int, session: Session):
    """Retorna um usuario pelo ID"""

    db_user = await session.scalar(select(User).where(
        or_(User.id == user_id,
            User.is_superuser == False))
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
async def create_user(user: UserCreate, session: Session):
    """Cria  um novo usuario"""

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
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.patch(
    '/{user_id}',
    response_model=userPublic,
    status_code=HTTPStatus.OK,
    summary='Atualiza  informações do usuário',
)
async def update_user(user_id: int, user_update: UserUpdate, session: Session):
    """
    Atualiza um ou mais campos do usuário (exceto username, email e password).
    Só os campos enviados no body serão atualizados.
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

    await session.commit()
    await session.refresh(db_user)
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
async def update_user_is_active(
    user_id: int, is_active_update: UserIsActiveUpdate, session: Session
):
    db_user = await session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    db_user.is_active = is_active_update.is_active
    await session.commit()
    await session.refresh(db_user)
    return db_user


# PATCH para atualizar is_verified
@router.patch(
    '/{user_id}/is_verified',
    response_model=userPublic,
    status_code=HTTPStatus.OK,
    summary='Atualiza o status de verificação do usuário',
)
async def update_user_is_verified(
    user_id: int, is_verified_update: UserIsVerifiedUpdate, session: Session
):
    db_user = await session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    try:
        db_user.is_verified = is_verified_update.is_verified
        await session.commit()
        await session.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail='Erro ao atualizar o status de verificação do usuário.',
        ) from e


# DELETE para deletar um usuário
@router.delete(
    '/{user_id}', status_code=HTTPStatus.NO_CONTENT, summary='Deleta usuário'
)
async def delete_user(
    user_id: int, session: Session, current_user: CurrentUser
):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )

    await session.delete(db_user)
    await session.commit()
