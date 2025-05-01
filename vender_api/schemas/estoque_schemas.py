from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


# Schemas para Entradas e Saídas de Estoque
class EntradaEstoqueBase(BaseModel):
    produto_sku: str = Field(
        ..., description='SKU do produto', example='ABC123'
    )
    quantidade: int = Field(
        ..., ge=1, description='Quantidade de entrada', example=10
    )
    data_entrada: datetime = Field(
        ..., description='Data e hora da entrada', example='2025-05-01T15:00:00'
    )
    observacao: Optional[str] = Field(
        None, description='Observação', max_length=255, example='Recebido sem avarias.'
    )

class EntradaEstoquePublic(EntradaEstoqueBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SaidaEstoqueBase(BaseModel):
    produto_sku: str = Field(
        ..., description='SKU do produto', example='ABC123'
    )
    quantidade: int = Field(
        ..., ge=1, description='Quantidade de saída', example=2
    )
    data_saida: datetime = Field(
        ..., description='Data e hora da saída', example='2025-05-01T16:00:00'
    )
    observacao: Optional[str] = Field(
        None, description='Observação', max_length=255, example='Saída para cliente X.'
    )



class SaidaEstoquePublic(SaidaEstoqueBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class EstoqueBase(BaseModel):
    produto_sku: str = Field(
        ..., description='SKU do produto', example='ABC123'
    )
    quantidade: int = Field(
        ..., ge=0, description='Quantidade em estoque', example=100
    )
    fornecedor_id: Optional[int] = Field(
        None, description='ID do fornecedor', example=1
    )
    lote: Optional[str] = Field(
        None, description='Lote do produto', max_length=50, example='L2025-01'
    )
    numero_serie: Optional[str] = Field(
        None, description='Número de série', max_length=100, example='SN123456789'
    )
    observacao: Optional[str] = Field(
        None, description='Observação', max_length=255, example='Estoque inicial.'
    )


class EstoqueUpdate(BaseModel):
    quantidade: Optional[int] = Field(None, ge=0, example=50)
    fornecedor_id: Optional[int] = Field(None, example=1)
    lote: Optional[str] = Field(None, max_length=50, example='L2025-01')
    numero_serie: Optional[str] = Field(None, max_length=100, example='SN123456789')
    observacao: Optional[str] = Field(None, max_length=255, example='Atualização de estoque.')


class EstoquePublic(EstoqueBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
