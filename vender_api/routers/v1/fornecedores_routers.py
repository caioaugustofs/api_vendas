from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session
from vender_api.models import Fornecedor
from vender_api.schemas.fornecedor_schemas import (
    FornecedorCreate,
    FornecedorPublic,
    FornecedorUpdate,
)
from vender_api.tools.decorador import commit_and_refresh

router = APIRouter(prefix='/fornecedores', tags=['Fornecedores'])

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get(
    '/', response_model=list[FornecedorPublic], status_code=HTTPStatus.OK
)
async def get_fornecedores(session: Session):
    """
    Retorna todos os registros de fornecedores.
    Essa rota é útil para listar todos os fornecedores cadastrados no sistema.

    Parâmetros:
        - Nenhum parâmetro de rota.

    Retorna:
        Lista de registros de fornecedores.
    """
    db_fornecedores = await session.execute(select(Fornecedor))
    return db_fornecedores.scalars().all()


@router.get(
    '/{fornecedor_id}',
    response_model=FornecedorPublic,
    status_code=HTTPStatus.OK,
)
async def get_fornecedor_by_id(fornecedor_id: int, session: Session):
    """
    Retorna um fornecedor específico pelo seu ID.
    Essa rota é útil para obter informações detalhadas sobre um fornecedor específico.

    Parâmetros:
        - fornecedor_id: ID do fornecedor a ser buscado.

    Retorna:
        Fornecedor correspondente ao ID informado.

    Erros:
        - 404: Fornecedor não encontrado.
    """
    db_fornecedor = await session.scalar(
        select(Fornecedor).where(Fornecedor.id == fornecedor_id)
    )
    if not db_fornecedor:
        raise HTTPException(
            status_code=404, detail='Fornecedor não encontrado'
        )
    return db_fornecedor


@router.post(
    '/', response_model=FornecedorPublic, status_code=HTTPStatus.CREATED
)
@commit_and_refresh(
    status_code=400,
    detail='Erro ao criar o fornecedor',
)
async def create_fornecedor(fornecedor: FornecedorCreate, session: Session):
    """
    Cria um novo registro de fornecedor.
    Essa rota é utilizada para cadastrar um novo fornecedor no sistema.

    Parâmetros:
        - fornecedor: Objeto contendo os dados necessários para criação do fornecedor.

    Retorna:
        O fornecedor criado com seus respectivos dados.

    Erros:
        - 400: Erro ao criar o fornecedor.
    """
    new_fornecedor = Fornecedor(**fornecedor.dict())
    session.add(new_fornecedor)
    return new_fornecedor


@router.patch(
    '/{fornecedor_id}',
    response_model=FornecedorPublic,
    status_code=HTTPStatus.OK,
)
@commit_and_refresh(
    status_code=400,
    detail='Erro ao atualizar o fornecedor',
)
async def update_fornecedor(
    fornecedor_id: int, fornecedor_update: FornecedorUpdate, session: Session
):
    """
    Atualiza campos de um registro de fornecedor.
    Essa rota permite atualizar informações específicas de um fornecedor já cadastrado.

    Parâmetros:
        - fornecedor_id: ID do fornecedor a ser atualizado.
        - fornecedor_update: Objeto com os campos a serem atualizados.

    Retorna:
        O fornecedor atualizado.

    Erros:
        - 404: Fornecedor não encontrado.
        - 400: Erro ao atualizar o fornecedor.
    """
    db_fornecedor = await session.scalar(
        select(Fornecedor).where(Fornecedor.id == fornecedor_id)
    )
    if not db_fornecedor:
        raise HTTPException(
            status_code=404, detail='Fornecedor não encontrado'
        )
    update_data = fornecedor_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_fornecedor, field, value)
    return db_fornecedor


@router.delete('/{fornecedor_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_fornecedor(fornecedor_id: int, session: Session):
    """
    Remove um registro de fornecedor.
    Essa rota é utilizada para excluir um fornecedor do sistema.

    Parâmetros:
        - fornecedor_id: ID do fornecedor a ser removido.

    Retorna:
        Nenhum conteúdo (status 204).

    Erros:
        - 404: Fornecedor não encontrado.
    """
    db_fornecedor = await session.scalar(
        select(Fornecedor).where(Fornecedor.id == fornecedor_id)
    )
    if not db_fornecedor:
        raise HTTPException(
            status_code=404, detail='Fornecedor não encontrado'
        )
    await session.delete(db_fornecedor)
    await session.commit()
