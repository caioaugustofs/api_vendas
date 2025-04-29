from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session

router = APIRouter(prefix='/users', tags=['users'])


Session_my = Annotated[AsyncSession, Depends(get_session)]


@router.get(
    '/',
)
async def get_users(session: Session_my): ...
