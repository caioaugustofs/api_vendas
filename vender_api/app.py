from http import HTTPStatus

from fastapi import FastAPI

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
def create_product(produto: ProdutosSchema): ...


@app.put('/produtos/{produto_id}', response_model=ProdutosPublic)
def update_product(produto_id: int, produto: ProdutosSchema): ...


@app.delete('/produtos/{produto_id}')
def delete_product(produto_id: int):
    return {'message': 'Produto deletado com sucesso!'}
