from typing import List
from pydantic import BaseModel

class CategoriaCreate(BaseModel):
    nome: str

class CategoriaRead(BaseModel):
    id: int
    nome: str
    class Config:
        orm_mode = True

class SubCategoriaCreate(BaseModel):
    nome: str
    categoria_id: int


class SubCategoriaRead(BaseModel):
    id: int
    nome: str
    categoria_id: int
    class Config:
        orm_mode = True

# Schema para resposta: categoria + lista de subcategorias
class CategoriaComSubcategorias(BaseModel):
    id: int
    nome: str
    subcategorias: List[SubCategoriaRead]
    class Config:
        orm_mode = True