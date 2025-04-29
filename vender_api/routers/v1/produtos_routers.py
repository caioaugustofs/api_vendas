from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from vender_api.database import get_session
from vender_api.models import Produtos
from vender_api.schemas.produtos_schemas import (
    ProdutosPublic,
    ProdutosSchema,
)

router = APIRouter(prefix='/produtos', tags=['produtos'])

from typing import Annotated

Session_my = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=list[ProdutosPublic])
def get_products(session: Session_my):
    produtos = session.execute(select(Produtos)).scalars().all()
    return produtos


@router.post(
    '/produtos/', status_code=HTTPStatus.CREATED, response_model=ProdutosPublic
)
def create_product(
    produto: ProdutosSchema, session: Session_my
):
    db_produto = session.scalar(
        select(Produtos).where(Produtos.sku == produto.sku)
    )

    if db_produto:
        if db_produto.sku == produto.sku:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Produto já cadastrado com esse SKU',
            )
    db_produto = Produtos(**produto.dict())
    session.add(db_produto)
    session.commit()
    session.refresh(db_produto)
    return db_produto


@router.put('/produtos/{produto_id}', response_model=ProdutosPublic)
def update_product(produto_id: int, produto: ProdutosSchema): ...


@router.delete('/produtos/{produto_id}')
def delete_product(produto_id: int):
    return {'message': 'Produto deletado com sucesso!'}
