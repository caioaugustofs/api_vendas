from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session
from vender_api.models import Categoria, Subcategoria
from vender_api.schemas.categoria_schemas import (
    CategoriaCreate,
    CategoriaPublic,
    SubcategoriaCreate,
    SubcategoriaPublic,
)
from vender_api.tools.decorador import commit_and_refresh

router = APIRouter(prefix='/categorias', tags=['Categorias'])
Session = Annotated[AsyncSession, Depends(get_session)]

# CATEGORIA
@router.get(
    '/', response_model=list[CategoriaPublic], status_code=HTTPStatus.OK
)
async def get_categorias(session: Session):
    db_categorias = await session.execute(select(Categoria))
    return db_categorias.scalars().all()


@router.get(
    '/{categoria_id}',
    response_model=CategoriaPublic,
    status_code=HTTPStatus.OK,
)
async def get_categoria_by_id(categoria_id: int, session: Session):
    db_categoria = await session.scalar(
        select(Categoria).where(Categoria.id == categoria_id)
    )
    if not db_categoria:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    return db_categoria


@router.post(
    '/', response_model=CategoriaPublic, status_code=HTTPStatus.CREATED
)
@commit_and_refresh(status_code=400, detail='Erro ao criar categoria')
async def create_categoria(categoria: CategoriaCreate, session: Session):
    new_categoria = Categoria(**categoria.dict())
    session.add(new_categoria)
    return new_categoria


# SUBCATEGORIA
@router.get(
    '/subcategorias/',
    response_model=list[SubcategoriaPublic],
    status_code=HTTPStatus.OK,
)
async def get_subcategorias(session: Session):
    db_subcategorias = await session.execute(select(Subcategoria))
    return db_subcategorias.scalars().all()


@router.get(
    '/subcategorias/{subcategoria_id}',
    response_model=SubcategoriaPublic,
    status_code=HTTPStatus.OK,
)
async def get_subcategoria_by_id(subcategoria_id: int, session: Session):
    db_subcategoria = await session.scalar(
        select(Subcategoria).where(Subcategoria.id == subcategoria_id)
    )
    if not db_subcategoria:
        raise HTTPException(
            status_code=404, detail='Subcategoria não encontrada'
        )
    return db_subcategoria


@router.post(
    '/subcategorias/',
    response_model=SubcategoriaPublic,
    status_code=HTTPStatus.CREATED,
)
@commit_and_refresh(status_code=400, detail='Erro ao criar subcategoria')
async def create_subcategoria(
    subcategoria: SubcategoriaCreate, session: Session
):
    new_subcategoria = Subcategoria(**subcategoria.dict())
    session.add(new_subcategoria)
    return new_subcategoria
