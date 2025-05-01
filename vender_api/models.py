from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

# Entradas de Estoque


table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    first_name: Mapped[str | None] = mapped_column(nullable=True, default=None)
    last_name: Mapped[str | None] = mapped_column(nullable=True, default=None)
    phone: Mapped[str | None] = mapped_column(nullable=True, default=None)
    address: Mapped[str | None] = mapped_column(nullable=True, default=None)
    city: Mapped[str | None] = mapped_column(nullable=True, default=None)
    state: Mapped[str | None] = mapped_column(nullable=True, default=None)
    country: Mapped[str | None] = mapped_column(nullable=True, default=None)
    zip_code: Mapped[str | None] = mapped_column(nullable=True, default=None)
    cpf: Mapped[str | None] = mapped_column(nullable=True, default=None)
    birth_date: Mapped[str | None] = mapped_column(nullable=True, default=None)
    cargo: Mapped[str | None] = mapped_column(nullable=True, default=None)


@table_registry.mapped_as_dataclass
class Produtos:
    __tablename__ = 'produtos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    sku: Mapped[str] = mapped_column(unique=True, nullable=False)
    nome: Mapped[str] = mapped_column()
    preco: Mapped[float] = mapped_column()
    ativo: Mapped[bool] = mapped_column(default=False)
    fabricante: Mapped[str | None] = mapped_column(nullable=True, default=None)
    categoria_id: Mapped[int | None] = mapped_column(
        nullable=True, default=None
    )
    subcategoria_id: Mapped[int | None] = mapped_column(
        nullable=True, default=None
    )
    dimensao: Mapped[str | None] = mapped_column(nullable=True, default=None)
    peso: Mapped[float | None] = mapped_column(nullable=True, default=None)
    descricao: Mapped[str | None] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Estoque:
    __tablename__ = 'estoque'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    produto_sku: Mapped[str] = mapped_column(ForeignKey('produtos.sku'))
    quantidade: Mapped[int] = mapped_column()
    fornecedor_id: Mapped[int | None] = mapped_column(
        nullable=True, default=None
    )
    lote: Mapped[str | None] = mapped_column(nullable=True, default=None)
    numero_serie: Mapped[str | None] = mapped_column(
        nullable=True, default=None
    )
    observacao: Mapped[str | None] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Fornecedor:
    __tablename__ = 'fornecedores'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column()
    cnpj: Mapped[str] = mapped_column(unique=True)
    inscricao_estadual: Mapped[str | None] = mapped_column(
        nullable=True, default=None
    )
    endereco: Mapped[str | None] = mapped_column(nullable=True, default=None)
    cidade: Mapped[str | None] = mapped_column(nullable=True, default=None)
    estado: Mapped[str | None] = mapped_column(nullable=True, default=None)
    pais: Mapped[str | None] = mapped_column(nullable=True, default=None)
    cep: Mapped[str | None] = mapped_column(nullable=True, default=None)
    telefone: Mapped[str | None] = mapped_column(nullable=True, default=None)
    email: Mapped[str | None] = mapped_column(nullable=True, default=None)


@table_registry.mapped_as_dataclass
class EntradaEstoque:
    __tablename__ = 'entradas_estoque'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    produto_sku: Mapped[str] = mapped_column(ForeignKey('produtos.sku'))
    quantidade: Mapped[int] = mapped_column()
    data_entrada: Mapped[datetime] = mapped_column()
    observacao: Mapped[str | None] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


# Saídas de Estoque
@table_registry.mapped_as_dataclass
class SaidaEstoque:
    __tablename__ = 'saidas_estoque'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    produto_sku: Mapped[str] = mapped_column(ForeignKey('produtos.sku'))
    quantidade: Mapped[int] = mapped_column()
    data_saida: Mapped[datetime] = mapped_column()
    observacao: Mapped[str | None] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
