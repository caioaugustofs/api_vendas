# Endpoint: retorna uma categoria e suas subcategorias
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from vender_api.database import get_session
from vender_api.models import Categoria, SubCategoria
from vender_api.schemas.categorias_schemas import (
    CategoriaCreate,
    CategoriaRead,
    SubCategoriaCreate,
    SubCategoriaRead,
    CategoriaComSubcategorias,
)

router = APIRouter(prefix="/categorias", tags=["categorias"])


# Rotas Categoria
@router.post("/", response_model=CategoriaRead)
async def create_categoria(categoria: CategoriaCreate,
                            session: AsyncSession = Depends(get_session)):
    """
    ## Cria uma nova categoria

    Cria uma categoria no sistema a partir dos dados fornecidos.

    **Parâmetros:**
    - `categoria` (`CategoriaCreate`): Dados para criação da categoria.

    **Retorno:**
    - `CategoriaRead`: Dados da categoria criada.

    **Status Codes:**
    - `201`: Categoria criada com sucesso.
    - `400`: Dados inválidos.

    **Exemplo de request:**
    ```json
    {
      "nome": "Eletrônicos"
    }
    ```

    **Exemplo de response:**
    ```json
    {
      "id": 1,
      "nome": "Eletrônicos"
    }
    ```
    """
    db_categoria = Categoria(nome=categoria.nome)
    session.add(db_categoria)
    await session.commit()
    await session.refresh(db_categoria)
    return db_categoria


@router.get("/", response_model=List[CategoriaRead])
async def list_categorias(session: AsyncSession = Depends(get_session)):
    """
    ## Recupera todas as categorias

    Retorna uma lista de todas as categorias cadastradas no sistema.

    **Retorno:**
    - `List[CategoriaRead]`: Lista de todas as categorias cadastradas.

    **Status Codes:**
    - `200`: Sucesso.

    **Exemplo de response:**
    ```json
    [
      {"id": 1, "nome": "Eletrônicos"},
      {"id": 2, "nome": "Roupas"}
    ]
    ```
    """
    result = await session.execute(select(Categoria))
    return result.scalars().all()


@router.get("/{categoria_id}", response_model=CategoriaRead)
async def get_categoria(categoria_id: int,
                        session: AsyncSession = Depends(get_session)):
    """
    ## Recupera uma categoria pelo seu ID

    Retorna os dados de uma categoria específica a partir do seu ID.

    **Parâmetros:**
    - `categoria_id` (`int`): O ID da categoria a ser buscada.

    **Retorno:**
    - `CategoriaRead`: Dados da categoria encontrada.

    **Status Codes:**
    - `200`: Sucesso.
    - `404`: Categoria não encontrada.

    **Exemplo de response:**
    ```json
    {
      "id": 1,
      "nome": "Eletrônicos"
    }
    ```
    """
    categoria = await session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404,
                             detail="Categoria não encontrada")
    return categoria


@router.patch("/{categoria_id}", response_model=CategoriaRead)
async def update_categoria(categoria_id: int,
                            categoria: CategoriaCreate,
                            session: AsyncSession = Depends(get_session)):
    
    """
    ## Atualiza uma categoria existente

    Atualiza os dados de uma categoria existente a partir do seu ID.

    **Parâmetros:**
    - `categoria_id` (`int`): O ID da categoria a ser atualizada.
    - `categoria` (`CategoriaCreate`): Novos dados para a categoria.

    **Retorno:**
    - `CategoriaRead`: Dados da categoria atualizada.

    **Status Codes:**
    - `200`: Categoria atualizada com sucesso.
    - `404`: Categoria não encontrada.

    **Exemplo de request:**
    ```json
    {
      "nome": "Eletrodomésticos"
    }
    ```

    **Exemplo de response:**
    ```json
    {
      "id": 1,
      "nome": "Eletrodomésticos"
    }
    ```
    """
    db_categoria = await session.get(Categoria, categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404,
                             detail="Categoria não encontrada")
    db_categoria.nome = categoria.nome
    await session.commit()
    await session.refresh(db_categoria)
    return db_categoria


@router.delete("/{categoria_id}")
async def delete_categoria(categoria_id: int,
                           session: AsyncSession = Depends(get_session)):
    
    """
    ## Deleta uma categoria existente

    Remove uma categoria do sistema a partir do seu ID.

    **Parâmetros:**
    - `categoria_id` (`int`): O ID da categoria a ser deletada.

    **Retorno:**
    - `dict`: Mensagem de sucesso.

    **Status Codes:**
    - `200`: Categoria deletada com sucesso.
    - `404`: Categoria não encontrada.

    **Exemplo de response:**
    ```json
    {"message": "Categoria deletada com sucesso"}
    ```
    """
    db_categoria = await session.get(Categoria, categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    await session.delete(db_categoria)
    await session.commit()
    return {"message": "Categoria deletada com sucesso"}


# Rotas SubCategoria
@router.post("/subcategorias/", response_model=SubCategoriaRead)
async def create_subcategoria(subcategoria: SubCategoriaCreate,
                               session: AsyncSession = Depends(get_session)):
    """
    ## Cria uma nova subcategoria

    Cria uma subcategoria vinculada a uma categoria existente.

    **Parâmetros:**
    - `subcategoria` (`SubCategoriaCreate`): Dados para criação da subcategoria.

    **Retorno:**
    - `SubCategoriaRead`: Dados da subcategoria criada.

    **Status Codes:**
    - `201`: Subcategoria criada com sucesso.
    - `400`: Dados inválidos.

    **Exemplo de request:**
    ```json
    {
      "nome": "Smartphones",
      "categoria_id": 1
    }
    ```

    **Exemplo de response:**
    ```json
    {
      "id": 1,
      "nome": "Smartphones",
      "categoria_id": 1
    }
    ```
    """
    db_subcategoria = SubCategoria(nome=subcategoria.nome,
                                   categoria_id=subcategoria.categoria_id)
    session.add(db_subcategoria)
    await session.commit()
    await session.refresh(db_subcategoria)
    return db_subcategoria


@router.get("/subcategorias/", response_model=List[SubCategoriaRead])
async def list_subcategorias(session: AsyncSession = Depends(get_session)):
    """
    ## Recupera todas as subcategorias

    Retorna uma lista de todas as subcategorias cadastradas no sistema.

    **Retorno:**
    - `List[SubCategoriaRead]`: Lista de todas as subcategorias cadastradas.

    **Status Codes:**
    - `200`: Sucesso.

    **Exemplo de response:**
    ```json
    [
      {"id": 1, "nome": "Smartphones", "categoria_id": 1},
      {"id": 2, "nome": "Notebooks", "categoria_id": 1}
    ]
    ```
    """
    result = await session.execute(select(SubCategoria))
    return result.scalars().all()


@router.get("/subcategorias/{subcategoria_id}",
            response_model=SubCategoriaRead)
async def get_subcategoria(subcategoria_id: int,
                           session: AsyncSession = Depends(get_session)):
    """
    ## Recupera uma subcategoria pelo seu ID

    Retorna os dados de uma subcategoria específica a partir do seu ID.

    **Parâmetros:**
    - `subcategoria_id` (`int`): O ID da subcategoria a ser buscada.

    **Retorno:**
    - `SubCategoriaRead`: Dados da subcategoria encontrada.

    **Status Codes:**
    - `200`: Sucesso.
    - `404`: SubCategoria não encontrada.

    **Exemplo de response:**
    ```json
    {
      "id": 1,
      "nome": "Smartphones",
      "categoria_id": 1
    }
    ```
    """
    subcategoria = await session.get(SubCategoria, subcategoria_id)
    if not subcategoria:
        raise HTTPException(status_code=404,
                            detail="SubCategoria não encontrada")
    return subcategoria


@router.patch("/subcategorias/{subcategoria_id}",
              response_model=SubCategoriaRead)
async def update_subcategoria(subcategoria_id: int,
                              subcategoria: SubCategoriaCreate,
                              session: AsyncSession = Depends(get_session)):
    """
    ## Atualiza uma subcategoria existente

    Atualiza os dados de uma subcategoria existente a partir do seu ID.

    **Parâmetros:**
    - `subcategoria_id` (`int`): O ID da subcategoria a ser atualizada.
    - `subcategoria` (`SubCategoriaCreate`): Novos dados para a subcategoria.

    **Retorno:**
    - `SubCategoriaRead`: Dados da subcategoria atualizada.

    **Status Codes:**
    - `200`: Subcategoria atualizada com sucesso.
    - `404`: SubCategoria não encontrada.

    **Exemplo de request:**
    ```json
    {
      "nome": "Notebooks",
      "categoria_id": 1
    }
    ```

    **Exemplo de response:**
    ```json
    {
      "id": 1,
      "nome": "Notebooks",
      "categoria_id": 1
    }
    ```
    """
    db_subcategoria = await session.get(SubCategoria, subcategoria_id)
    if not db_subcategoria:
        raise HTTPException(status_code=404,
                             detail="SubCategoria não encontrada")
    db_subcategoria.nome = subcategoria.nome
    db_subcategoria.categoria_id = subcategoria.categoria_id
    await session.commit()
    await session.refresh(db_subcategoria)
    return db_subcategoria


@router.delete("/subcategorias/{subcategoria_id}")
async def delete_subcategoria(subcategoria_id: int,
                              session: AsyncSession = Depends(get_session)):
    """
    ## Deleta uma subcategoria existente

    Remove uma subcategoria do sistema a partir do seu ID.

    **Parâmetros:**
    - `subcategoria_id` (`int`): O ID da subcategoria a ser deletada.

    **Retorno:**
    - `dict`: Mensagem de sucesso.

    **Status Codes:**
    - `200`: Subcategoria deletada com sucesso.
    - `404`: SubCategoria não encontrada.

    **Exemplo de response:**
    ```json
    {"message": "SubCategoria deletada com sucesso"}
    ```
    """
    db_subcategoria = await session.get(SubCategoria, subcategoria_id)
    if not db_subcategoria:
        raise HTTPException(status_code=404,
                            detail="SubCategoria não encontrada")
    await session.delete(db_subcategoria)
    await session.commit()
    return {"message": "SubCategoria deletada com sucesso"}

