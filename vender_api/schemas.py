from pydantic import BaseModel


class Message(BaseModel):
    message: str


class ProdutosSchema(BaseModel):
    id: int
    sku: str
    nome: str
    frabricante: str
    id_fabricante: str
    categoria: str
    peso: float
    dimensao: str
    ativo: bool


class ProdutosPublic(BaseModel):
    id: int
    sku: str
    nome: str
    ativo: bool

    class Config:
        orm_mode = True


class ProdutosList(BaseModel):
    produtos: list[ProdutosPublic]
