from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SubcategoriaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = Field(None, max_length=255)


class SubcategoriaCreate(SubcategoriaBase):
    categoria_id: int


class SubcategoriaPublic(SubcategoriaBase):
    id: int
    categoria_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CategoriaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = Field(None, max_length=255)


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaPublic(CategoriaBase):
    id: int
    subcategorias: List[SubcategoriaPublic] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
