from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EstoqueBase(BaseModel):
    produto_sku: str = Field(...,
                             description='SKU do produto')
    quantidade: int = Field(..., ge=0,
                            description='Quantidade em estoque')
    preco_de_aquisicao: float = Field(...,
                                       ge=0, description='Preço de aquisição')
    data_de_aquisicao: datetime = Field(...,
                                         description='Data de aquisição')


class EstoqueCreate(EstoqueBase):
    pass


class EstoqueUpdate(BaseModel):
    quantidade: Optional[int] = Field(None, ge=0)
    preco_de_aquisicao: Optional[float] = Field(None, ge=0)
    data_de_aquisicao: Optional[datetime] = None
    fornecedor_id: Optional[int] = None
    lote: Optional[str] = None
    numero_serie: Optional[str] = None
    observacao: Optional[str] = None


class EstoquePublic(EstoqueBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
