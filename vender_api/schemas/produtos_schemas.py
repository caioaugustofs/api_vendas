from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProdutoBase(BaseModel):
    """Campos obrigatórios do produto."""

    sku: str = Field(
        ...,
        min_length=3,
        max_length=32,
        description='SKU do produto',
        example='ABC123',
    )
    nome: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description='Nome do produto',
        example='Notebook Gamer',
    )
    preco: float = Field(
        ..., ge=0, description='Preço do produto', example=1999.99
    )
    ativo: bool = Field(default=False, description='Produto ativo')


class ProdutoCreate(BaseModel):
    """Schema para criação de produtos."""

    sku: str = Field(
        ...,
        min_length=3,
        max_length=32,
        description='SKU do produto',
        example='ABC123',
    )
    nome: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description='Nome do produto',
        example='Notebook Gamer',
    )
    preco: float = Field(
        ..., ge=0, description='Preço do produto', example=1999.99
    )
    ativo: bool = Field(default=False, description='Produto ativo')
    fabricante: Optional[str] = Field(
        None, max_length=100, description='Nome do fabricante', example='Dell'
    )
    categoria_id: Optional[int] = Field(
        None, description='ID da categoria', example=1
    )
    subcategoria_id: Optional[int] = Field(
        None, description='ID da subcategoria', example=2
    )
    dimensao: Optional[str] = Field(
        None,
        max_length=50,
        description='Dimensões do produto',
        example='30x20x5cm',
    )
    peso: Optional[float] = Field(
        None, ge=0, description='Peso do produto em kg', example=2.5
    )
    descricao: Optional[str] = Field(
        None,
        max_length=255,
        description='Descrição do produto',
        example='Notebook de alto desempenho.',
    )


class ProdutoUpdate(BaseModel):
    """Schema para atualização parcial de produtos (todos opcionais)."""

    sku: Optional[str] = Field(
        None,
        min_length=3,
        max_length=32,
        description='SKU do produto',
        example='ABC123',
    )
    nome: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description='Nome do produto',
        example='Notebook Gamer',
    )
    preco: Optional[float] = Field(
        None, ge=0, description='Preço do produto', example=1999.99
    )
    ativo: Optional[bool] = Field(None, description='Produto ativo')
    fabricante: Optional[str] = Field(
        None, max_length=100, description='Nome do fabricante', example='Dell'
    )
    categoria_id: Optional[int] = Field(
        None, description='ID da categoria', example=1
    )
    subcategoria_id: Optional[int] = Field(
        None, description='ID da subcategoria', example=2
    )
    dimensao: Optional[str] = Field(
        None,
        max_length=50,
        description='Dimensões do produto',
        example='30x20x5cm',
    )
    peso: Optional[float] = Field(
        None, ge=0, description='Peso do produto em kg', example=2.5
    )
    descricao: Optional[str] = Field(
        None,
        max_length=255,
        description='Descrição do produto',
        example='Notebook de alto desempenho.',
    )


class ProdutoPublic(BaseModel):
    """Schema público de produto, usado em respostas."""

    id: int
    sku: str
    nome: str
    preco: float
    ativo: bool
    fabricante: Optional[str] = None
    categoria_id: Optional[int] = None
    subcategoria_id: Optional[int] = None
    dimensao: Optional[str] = None
    peso: Optional[float] = None
    descricao: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


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
