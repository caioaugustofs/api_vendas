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
    """
    Retorna uma lista de todos os produtos cadastrados no banco de dados.
    """
    result = await session.execute(select(Produtos))
    produtos = result.scalars().all()
    return produtos


# rota para buscar um produto pelo id ou sku
@router.get('/{produto_id}', response_model=ProdutosPublic)
async def get_product(produto_id: int, session: Session_my):
    """
    Busca e retorna um produto específico pelo seu ID.
    Se não encontrar, retorna erro 404.
    """
    result = await session.execute(
        select(Produtos).where(Produtos.id == produto_id)
    )
    db_produto = result.scalar_one_or_none()
    if not db_produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Produto não encontrado',
        )
    return db_produto


# rota para buscar um produto pelo sku
@router.get('/sku/{sku}', response_model=ProdutosPublic)
async def get_product_by_sku(sku: str, session: Session_my):
    """
    Busca e retorna um produto específico pelo seu SKU.
    Se não encontrar, retorna erro 404.
    """
    result = await session.execute(select(Produtos).where(Produtos.sku == sku))
    db_produto = result.scalar_one_or_none()
    if not db_produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Produto não encontrado',
        )
    return db_produto


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=ProdutosPublic
)
async def create_product(produto: ProdutosSchema, session: Session_my):
    """
    Cria um novo produto com os dados enviados no corpo da requisição.
    Se já existir um produto com o mesmo SKU, retorna erro 409 (conflito).
    """
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


# rota para atualizar o  se o prodito esta ativo ou inativo
@router.patch(
    '/{produto_id}/{ativar_desativar}', response_model=ProdutosPublic
)
async def update_product_status(
    produto_id: int, ativar_desativar: bool, session: Session_my
):
    """
    Ativa ou desativa um produto, alterando o campo 'ativo'.
    conforme o valor booleano enviado na URL (ativar_desativar).
    Se o produto não existir, retorna erro 404.
    """
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


@router.delete('/{produto_id}')
async def delete_product(produto_id: int, session: Session_my):
    """
    Remove um produto do banco de dados pelo seu ID.
    Se não encontrar, retorna erro 404.
    Se deletar com sucesso, retorna uma mensagem de confirmação.
    """
    db_produto = await session.get(Produtos, produto_id)
    if not db_produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Produto não encontrado',
        )
    await session.delete(db_produto)
    await session.commit()
    return {'message': 'Produto deletado com sucesso'}
