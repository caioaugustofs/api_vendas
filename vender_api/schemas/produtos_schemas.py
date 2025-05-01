
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProdutoBase(BaseModel):
    sku: str = Field(..., description='SKU do produto')
    nome: str = Field(..., description='Nome do produto')
    preco: float = Field(..., ge=0, description='Preço do produto')
    ativo: bool = Field(default=False, description='Produto ativo')


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = Field(None, ge=0)
    ativo: Optional[bool] = None
    fabricante: Optional[str] = None
    categoria_id: Optional[int] = None
    subcategoria_id: Optional[int] = None
    dimensao: Optional[str] = None
    peso: Optional[float] = None
    descricao: Optional[str] = None


class ProdutoPublic(ProdutoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
