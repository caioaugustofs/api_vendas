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
from vender_api.tools.decorador import commit_and_refresh

router = APIRouter(prefix='/estoque', tags=['Estoque'])

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get('/', response_model=list[EstoquePublic], status_code=HTTPStatus.OK)
async def get_estoques(session: Session):
    """
    Retorna todos os registros de estoque.
    Essa rota é útil para listar todos os estoques cadastrados no sistema.

    Parâmetros:
        - Nenhum parâmetro de rota.

    Retorna:
        Lista de registros de estoque.

    Exemplo de resposta:
        [
            {
                "id": 1,
                "produto_id": 10,
                "quantidade": 100
            },
            ...
        ]
    """
    db_estoques = await session.execute(select(Estoque))
    return db_estoques.scalars().all()


@router.get(
    '/{estoque_id}', response_model=EstoquePublic, status_code=HTTPStatus.OK
)
async def get_estoque_by_id(
    estoque_id: int, session: Session, skip: int = 0, limit: int = 100
):
    """
    Retorna um estoque específico pelo seu ID.
    Essa rota é útil para obter informações detalhadas sobre um estoque específico.

    Parâmetros:
        - estoque_id: ID do estoque a ser buscado.
        - skip: Quantidade de registros a pular (padrão: 0).
        - limit: Limite de registros retornados (padrão: 100).

    Retorna:
        Estoque correspondente ao ID informado.

    Erros:
        - 404: Estoque não encontrado.
    """
    db_estoque = await session.scalar(
        select(Estoque)
        .where(Estoque.id == estoque_id)
        .offset(skip)
        .limit(limit)
    )
    if not db_estoque:
        raise HTTPException(status_code=404, detail='Estoque não encontrado')
    return db_estoque


@router.post('/', response_model=EstoquePublic, status_code=HTTPStatus.CREATED)
@commit_and_refresh(
    status_code=400,
    detail='Erro ao criar o estoque',
)
async def create_estoque(estoque: EstoqueCreate, session: Session):
    """
    Cria um novo registro de estoque.
    O estoque sempre inicia com quantidade 0. A movimentação é responsável por atualizar a quantidade.

    Parâmetros:
        - estoque: Objeto contendo os dados necessários para criação do estoque (exceto quantidade).

    Retorna:
        O estoque criado com quantidade 0.

    Erros:
        - 400: Erro ao criar o estoque.
    """
    data = estoque.dict()
    data['quantidade'] = 0  # Garante que sempre inicia em 0
    new_estoque = Estoque(**data)
    session.add(new_estoque)
    return new_estoque


@router.patch(
    '/{estoque_id}', response_model=EstoquePublic, status_code=HTTPStatus.OK
)
@commit_and_refresh(
    status_code=400,
    detail='Erro ao atualizar o estoque',
)
async def update_estoque(
    estoque_id: int, estoque_update: EstoqueUpdate, session: Session
):
    """
    Atualiza campos de um registro de estoque, exceto a quantidade.
    A quantidade só pode ser alterada via movimentação de estoque.

    Parâmetros:
        - estoque_id: ID do estoque a ser atualizado.
        - estoque_update: Objeto com os campos a serem atualizados (exceto quantidade).

    Retorna:
        O estoque atualizado.

    Erros:
        - 404: Estoque não encontrado.
        - 400: Erro ao atualizar o estoque.
    """
    db_estoque = await session.scalar(
        select(Estoque).where(Estoque.id == estoque_id)
    )
    if not db_estoque:
        raise HTTPException(status_code=404, detail='Estoque não encontrado')
    update_data = estoque_update.dict(exclude_unset=True)
    # Remover quantidade se vier no update
    update_data.pop('quantidade', None)
    for field, value in update_data.items():
        setattr(db_estoque, field, value)
    return db_estoque


@router.delete('/{estoque_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_estoque(estoque_id: int, session: Session):
    """
    Remove um registro de estoque.
    Essa rota é utilizada para excluir um estoque do sistema.

    Parâmetros:
        - estoque_id: ID do estoque a ser removido.

    Retorna:
        Nenhum conteúdo (status 204).

    Erros:
        - 404: Estoque não encontrado.
    """
    db_estoque = await session.scalar(
        select(Estoque).where(Estoque.id == estoque_id)
    )
    if not db_estoque:
        raise HTTPException(status_code=404, detail='Estoque não encontrado')
    await session.delete(db_estoque)
    await session.commit()
