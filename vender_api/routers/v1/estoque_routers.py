from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session
from vender_api.models import Estoque
from vender_api.schemas.estoque_schemas import (
    EstoqueCreate,
    EstoquePublic,
    EstoqueUpdate,
)

router = APIRouter(prefix='/estoque', tags=['Estoque'])

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get('/', response_model=list[EstoquePublic], status_code=HTTPStatus.OK)
async def get_estoques(session: Session):
    """Retorna todos os registros de estoque."""
    db_estoques = await session.execute(select(Estoque))
    return db_estoques.scalars().all()


@router.get('/{estoque_id}', response_model=EstoquePublic, status_code=HTTPStatus.OK)
async def get_estoque_by_id(estoque_id: int, session: Session):
    """Retorna um registro de estoque pelo ID."""
    db_estoque = await session.scalar(select(Estoque).where(Estoque.id == estoque_id))
    if not db_estoque:
        raise HTTPException(status_code=404, detail='Estoque não encontrado')
    return db_estoque


@router.post('/', response_model=EstoquePublic, status_code=HTTPStatus.CREATED)
async def create_estoque(estoque: EstoqueCreate, session: Session):
    """Cria um novo registro de estoque."""
    new_estoque = Estoque(**estoque.dict())
    session.add(new_estoque)
    await session.commit()
    await session.refresh(new_estoque)
    return new_estoque


@router.patch('/{estoque_id}', response_model=EstoquePublic, status_code=HTTPStatus.OK)
async def update_estoque(estoque_id: int, estoque_update: EstoqueUpdate, session: Session):
    """Atualiza campos de um registro de estoque."""
    db_estoque = await session.scalar(select(Estoque).where(Estoque.id == estoque_id))
    if not db_estoque:
        raise HTTPException(status_code=404, detail='Estoque não encontrado')
    update_data = estoque_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_estoque, field, value)
    await session.commit()
    await session.refresh(db_estoque)
    return db_estoque


@router.delete('/{estoque_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_estoque(estoque_id: int, session: Session):
    """Remove um registro de estoque."""
    db_estoque = await session.scalar(select(Estoque).where(Estoque.id == estoque_id))
    if not db_estoque:
        raise HTTPException(status_code=404, detail='Estoque não encontrado')
    await session.delete(db_estoque)
    await session.commit()
