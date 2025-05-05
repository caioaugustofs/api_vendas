from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class FornecedorBase(BaseModel):
    nome: str
    cnpj: Optional[int] = Field(
        None,
        alias='CNPJ',
        max_length=18,
    )
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None


class FornecedorCreate(FornecedorBase):
    pass


class FornecedorFull(BaseModel):
    id: int
    nome: str
    cnpj: Optional[int] = Field(None, alias='CNPJ', max_length=18)
    email: Optional[EmailStr] = Field(None, max_length=100)
    telefone: Optional[str] = Field(None, max_length=15)
    endereco: Optional[str] = Field(None, max_length=200)
    cidade: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=50)
    inscricao_estadual: Optional[str] = Field(None, max_length=20)
    pais: Optional[str] = Field(None, max_length=50)
    cep: Optional[str] = Field(None, max_length=10)


class FornecedorUpdate(BaseModel):
    nome: Optional[str] = None
    cnpj: Optional[int] = Field(None, alias='CNPJ', max_length=18)
    email: Optional[EmailStr] = Field(None, max_length=100)
    telefone: Optional[str] = Field(None, max_length=15)
    endereco: Optional[str] = Field(None, max_length=200)
    cidade: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=50)
    inscricao_estadual: Optional[str] = Field(None, max_length=20)
    pais: Optional[str] = Field(None, max_length=50)
    cep: Optional[str] = Field(None, max_length=10)


class FornecedorPublic(FornecedorBase):
    id: int

    class Config:
        orm_mode = True
