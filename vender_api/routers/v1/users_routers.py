from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session
from vender_api.models import User
from vender_api.schemas.users_schemas import UserCreate, userPublic

router = APIRouter(prefix='/users', tags=['users'])


Session = Annotated[AsyncSession, Depends(get_session)]


@router.get('/')
async def get_users(
    session: Session,
):
    db_users = await session.execute(select(User))
    return db_users.scalars().all()


@router.get('/{user_id}')
async def get_user_by_user(user_id: int, session: Session):
    """Retorna um usuario pelo ID"""

    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )

    return db_user


@router.post('/', response_model=userPublic)
async def create_user(user: UserCreate, session: Session):
    """cria  um novo usuario"""

    db_user = await session.scalar(
        select(User).where(
            User.username == user.username | User.email == user.email
        )
    )

    if db_user:
        raise HTTPException(
            status_code=400,
            detail='User already exists',
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
