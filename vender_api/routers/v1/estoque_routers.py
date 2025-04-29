from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session

router = APIRouter(prefix='/estoque', tags=['estoque'])


Session_my = Annotated[AsyncSession, Depends(get_session)]


@router.get('/', response_model=list[dict])
async def get_estoque(session: Session_my):
    ...
