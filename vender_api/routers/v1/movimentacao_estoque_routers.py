from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session
from vender_api.models import EntradaEstoque, Estoque, SaidaEstoque
from vender_api.schemas.estoque_schemas import (
    EntradaEstoqueCreate,
    EntradaEstoquePublic,
    SaidaEstoqueCreate,
    SaidaEstoquePublic,
)
from vender_api.tools.decorador import commit_and_refresh

router = APIRouter(prefix='/movimentacoes', tags=['Movimentações de Estoque'])

Session = Annotated[AsyncSession, Depends(get_session)]


# Rotas de Entrada de Estoque
@router.get(
    '/entradas',
    response_model=list[EntradaEstoquePublic],
    status_code=HTTPStatus.OK,
)
async def get_entradas_estoque(session: Session):
    """Retorna todas as entradas de estoque."""
    db_entradas = await session.execute(select(EntradaEstoque))
    return db_entradas.scalars().all()


@router.get(
    '/entradas/{entrada_id}',
    response_model=EntradaEstoquePublic,
    status_code=HTTPStatus.OK,
)
async def get_entrada_estoque_by_id(
    entrada_id: int, session: Session, skip: int = 0, limit: int = 100
):
    """Retorna uma entrada de estoque pelo ID."""
    db_entrada = await session.scalar(
        select(EntradaEstoque)
        .where(EntradaEstoque.id == entrada_id)
        .offset(skip)
        .limit(limit)
    )
    if not db_entrada:
        raise HTTPException(
            status_code=404, detail='Entrada de estoque não encontrada'
        )
    return db_entrada


@router.post(
    '/entradas',
    response_model=EntradaEstoquePublic,
    status_code=HTTPStatus.CREATED,
)
@commit_and_refresh(
    status_code=400,
    detail='Erro ao criar a entrada de estoque',
)
async def create_entrada_estoque(
    entrada: EntradaEstoqueCreate, session: Session
):
    """Cria uma nova entrada de estoque."""
    new_entrada = EntradaEstoque(**entrada.dict())
    session.add(new_entrada)
    # Atualiza ou cria saldo em Estoque

    db_estoque = await session.scalar(
        select(Estoque).where(Estoque.produto_sku == entrada.produto_sku)
    )
    if db_estoque:
        db_estoque.quantidade += entrada.quantidade
    else:
        db_estoque = Estoque(
            produto_sku=entrada.produto_sku,
            quantidade=entrada.quantidade,
        )
    session.add(db_estoque)
    return new_entrada


# Rotas de Saída de Estoque
@router.get(
    '/saidas',
    response_model=list[SaidaEstoquePublic],
    status_code=HTTPStatus.OK,
)
async def get_saidas_estoque(session: Session):
    """Retorna todas as saídas de estoque."""
    db_saidas = await session.execute(select(SaidaEstoque))
    return db_saidas.scalars().all()


@router.get(
    '/saidas/{saida_id}',
    response_model=SaidaEstoquePublic,
    status_code=HTTPStatus.OK,
)
async def get_saida_estoque_by_id(
    saida_id: int, session: Session, skip: int = 0, limit: int = 100
):
    """Retorna uma saída de estoque pelo ID."""
    db_saida = await session.scalar(
        select(SaidaEstoque)
        .where(SaidaEstoque.id == saida_id)
        .offset(skip)
        .limit(limit)
    )
    if not db_saida:
        raise HTTPException(
            status_code=404, detail='Saída de estoque não encontrada'
        )
    return db_saida


@router.post(
    '/saidas',
    response_model=SaidaEstoquePublic,
    status_code=HTTPStatus.CREATED,
)
@commit_and_refresh(
    status_code=400,
    detail='Erro ao criar a saída de estoque',
)
async def create_saida_estoque(saida: SaidaEstoqueCreate, session: Session):
    """Cria uma nova saída de estoque."""
    new_saida = SaidaEstoque(**saida.dict())
    session.add(new_saida)
    # Atualiza saldo em Estoque

    db_estoque = await session.scalar(
        select(Estoque).where(Estoque.produto_sku == saida.produto_sku)
    )
    if db_estoque and db_estoque.quantidade >= saida.quantidade:
        db_estoque.quantidade -= saida.quantidade
    else:
        raise HTTPException(
            status_code=400, detail='Estoque insuficiente para saída'
        )
    return new_saida
