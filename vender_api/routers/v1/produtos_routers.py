from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session
from vender_api.models import Produtos
from vender_api.schemas.produtos_schemas import (
    ProdutosPublic,
    ProdutosSchema,
)

router = APIRouter(prefix='/produtos', tags=['produtos'])


Session_my = Annotated[AsyncSession, Depends(get_session)]


@router.get('/', response_model=list[ProdutosPublic])
async def get_products(session: Session_my):
    result = await session.execute(select(Produtos))
    produtos = result.scalars().all()
    return produtos


@router.post(
    '/produtos/', status_code=HTTPStatus.CREATED, response_model=ProdutosPublic
)
async def create_product(produto: ProdutosSchema, session: Session_my):
    result = await session.execute(
        select(Produtos).where(Produtos.sku == produto.sku)
    )
    db_produto = result.scalar_one_or_none()

    if db_produto:
        if db_produto.sku == produto.sku:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Produto já cadastrado com esse SKU',
            )
    db_produto = Produtos(**produto.dict())
    session.add(db_produto)
    await session.commit()
    await session.refresh(db_produto)
    return db_produto


@router.put('/produtos/{produto_id}', response_model=ProdutosPublic)
async def update_product(
    produto_id: int, produto: ProdutosSchema, session: Session_my
):
    # Implementação futura
    pass


# rota para atualizar o  se o prodito esta ativo ou inativo
@router.patch(
    '/produtos/{produto_id}/{ativar_desativar}', response_model=ProdutosPublic
)
async def update_product_status(
    produto_id: int, ativar_desativar: bool, session: Session_my
):
    db_produto = await session.get(Produtos, produto_id)
    if not db_produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Produto não encontrado',
        )
    db_produto.ativo = ativar_desativar
    await session.commit()
    await session.refresh(db_produto)
    return db_produto


@router.delete('/produtos/{produto_id}')
async def delete_product(produto_id: int, session: Session_my):
    db_produto = await session.get(Produtos, produto_id)
    if not db_produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Produto não encontrado',
        )
    await session.delete(db_produto)
    await session.commit()
    return {'message': 'Produto deletado com sucesso'}
