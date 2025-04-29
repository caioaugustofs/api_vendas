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
    ## Recupera todos os produtos

    Retorna uma lista de todos os produtos cadastrados no banco de dados.

    **Retorno:**
    - `List[ProdutosPublic]`: Lista de todos os produtos cadastrados.

    **Status Codes:**
    - `200`: Sucesso.

    **Exemplo de response:**
    ```json
    [
      {"id": 1, "nome": "Notebook", "sku": "NB123", "ativo": true},
      {"id": 2, "nome": "Mouse", "sku": "MS456", "ativo": false}
    ]
    ```
    """
    result = await session.execute(select(Produtos))
    produtos = result.scalars().all()
    return produtos


# rota para buscar um produto pelo id ou sku
@router.get('/{produto_id}', response_model=ProdutosPublic)
async def get_product(produto_id: int, session: Session_my):
    """
    ## Recupera um produto pelo ID

    Retorna os dados de um produto específico a partir do seu ID.

    **Parâmetros:**
    - `produto_id` (`int`): O ID do produto a ser buscado.

    **Retorno:**
    - `ProdutosPublic`: Dados do produto encontrado.

    **Status Codes:**
    - `200`: Sucesso.
    - `404`: Produto não encontrado.

    **Exemplo de response:**
    ```json
    {
      "id": 1,
      "nome": "Notebook",
      "sku": "NB123",
      "ativo": true
    }
    ```
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
    ## Recupera um produto pelo SKU

    Retorna os dados de um produto específico a partir do seu SKU.

    **Parâmetros:**
    - `sku` (`str`): O SKU do produto a ser buscado.

    **Retorno:**
    - `ProdutosPublic`: Dados do produto encontrado.

    **Status Codes:**
    - `200`: Sucesso.
    - `404`: Produto não encontrado.

    **Exemplo de response:**
    ```json
    {
      "id": 1,
      "nome": "Notebook",
      "sku": "NB123",
      "ativo": true
    }
    ```
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
    ## Cria um novo produto

    Cria um novo produto com os dados enviados no corpo da requisição.

    **Parâmetros:**
    - `produto` (`ProdutosSchema`): Dados para criação do produto.

    **Retorno:**
    - `ProdutosPublic`: Dados do produto criado.

    **Status Codes:**
    - `201`: Produto criado com sucesso.
    - `400`: Dados inválidos.
    - `409`: Produto já cadastrado com esse SKU.

    **Exemplo de request:**
    ```json
    {
      "nome": "Notebook",
      "sku": "NB123",
      "ativo": true
    }
    ```

    **Exemplo de response:**
    ```json
    {
      "id": 1,
      "nome": "Notebook",
      "sku": "NB123",
      "ativo": true
    }
    ```
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
    ## Ativa ou desativa um produto

    Altera o status de ativo/inativo de um produto, conforme o valor booleano enviado na URL.

    **Parâmetros:**
    - `produto_id` (`int`): O ID do produto a ser atualizado.
    - `ativar_desativar` (`bool`): Define se o produto será ativado (`true`) ou desativado (`false`).

    **Retorno:**
    - `ProdutosPublic`: Dados do produto atualizado.

    **Status Codes:**
    - `200`: Produto atualizado com sucesso.
    - `404`: Produto não encontrado.

    **Exemplo de request:**
    PATCH /produtos/1/false

    **Exemplo de response:**
    ```json
    {
      "id": 1,
      "nome": "Notebook",
      "sku": "NB123",
      "ativo": false
    }
    ```
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
    ## Deleta um produto existente

    Remove um produto do banco de dados pelo seu ID.

    **Parâmetros:**
    - `produto_id` (`int`): O ID do produto a ser deletado.

    **Retorno:**
    - `dict`: Mensagem de sucesso.

    **Status Codes:**
    - `200`: Produto deletado com sucesso.
    - `404`: Produto não encontrado.

    **Exemplo de response:**
    ```json
    {"message": "Produto deletado com sucesso"}
    ```
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
