
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session
from vender_api.models import Produtos
from vender_api.schemas.produtos_schemas import (
    ProdutoCreate,
    ProdutoPublic,
    ProdutoUpdate,
)

router = APIRouter(prefix='/produtos', tags=['Produtos'])

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get('/', response_model=list[ProdutoPublic], status_code=HTTPStatus.OK)
async def get_produtos(session: Session):
    """Retorna todos os produtos."""
    db_produtos = await session.execute(select(Produtos))
    return db_produtos.scalars().all()


@router.get('/{produto_id}', response_model=ProdutoPublic, status_code=HTTPStatus.OK)
async def get_produto_by_id(produto_id: int, session: Session):
    """Retorna um produto pelo ID."""
    db_produto = await session.scalar(select(Produtos).where(Produtos.id == produto_id))
    if not db_produto:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return db_produto


@router.post('/', response_model=ProdutoPublic, status_code=HTTPStatus.CREATED)
async def create_produto(produto: ProdutoCreate, session: Session):
    """Cria um novo produto."""
    # Verifica se já existe produto com o mesmo SKU
    db_produto = await session.scalar(select(Produtos).where(Produtos.sku == produto.sku))
    if db_produto:
        raise HTTPException(status_code=400, detail='SKU já cadastrado')
    new_produto = Produtos(**produto.dict())
    session.add(new_produto)
    await session.commit()
    await session.refresh(new_produto)
    return new_produto


@router.patch('/{produto_id}', response_model=ProdutoPublic, status_code=HTTPStatus.OK)
async def update_produto(produto_id: int, produto_update: ProdutoUpdate, session: Session):
    """Atualiza campos de um produto."""
    db_produto = await session.scalar(select(Produtos).where(Produtos.id == produto_id))
    if not db_produto:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    update_data = produto_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_produto, field, value)
    await session.commit()
    await session.refresh(db_produto)
    return db_produto


@router.delete('/{produto_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_produto(produto_id: int, session: Session):
    """Remove um produto."""
    db_produto = await session.scalar(select(Produtos).where(Produtos.id == produto_id))
    if not db_produto:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    await session.delete(db_produto)
    await session.commit()
