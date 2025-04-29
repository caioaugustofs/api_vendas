from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from vender_api.database import get_session
from vender_api.models import Produtos
from vender_api.schemas import (
    Message,
    ProdutosPublic,
    ProdutosSchema,
)

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post(
    '/produtos/', status_code=HTTPStatus.CREATED, response_model=ProdutosPublic
)
def create_product(
    produto: ProdutosSchema, session: Session = Depends(get_session)
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


@app.put('/produtos/{produto_id}', response_model=ProdutosPublic)
def update_product(produto_id: int, produto: ProdutosSchema): ...


@app.delete('/produtos/{produto_id}')
def delete_product(produto_id: int):
    return {'message': 'Produto deletado com sucesso!'}
