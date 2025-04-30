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
from vender_api.security import get_password_hash

router = APIRouter(prefix='/users_root', tags=['users root'])


Session = Annotated[AsyncSession, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=userPublic)
async def create_user_root(user: UserCreate, session: Session):
    """Cria  um novo usuario"""
    # funcao funciona para criar um superuser   ele so funciona se
    # nao existir um usuario superuser
    # se existir um usuario superuser ele vai não criar um usuario

    db_superuser = await session.scalar(select(User).where(User.is_superuser))
    if db_superuser:
        raise HTTPException(
            status_code=400,
            detail='Superuser already exists',
        )

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

    hashed_password = get_password_hash(user.password)

    new_user_root = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        is_superuser=True,
        is_verified=True,
        is_active=True,
    )

    session.add(new_user_root)
    await session.commit()
    await session.refresh(new_user_root)
    return new_user_root


@router.get('/', response_model=list[userPublic], status_code=HTTPStatus.OK)
async def get_users_root(
    session: Session,
):
    """Retorna todos os usuarios"""
    db_users = await session.execute(select(User))
    return db_users.scalars().all()


@router.get('/{user_id}', status_code=HTTPStatus.OK)
async def get_user_by_user_root(user_id: int, session: Session):
    """Retorna um usuario pelo ID"""

    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )

    return db_user


@router.patch('/{user_id}/is_superuser', response_model=userPublic)
async def update_user_is_superuser(
    user_id: int, is_superuser_update: UserIsSuperuserUpdate, session: Session
):
    db_user = await session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    db_user.is_superuser = is_superuser_update.is_superuser
    await session.commit()
    await session.refresh(db_user)
    return db_user
