from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

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
class Categoria:
    __tablename__ = 'categorias'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    subcategorias: Mapped[list['SubCategoria']] = relationship(
        'SubCategoria', back_populates='categoria', init=False
    )


@table_registry.mapped_as_dataclass
class SubCategoria:
    __tablename__ = 'subcategorias'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column()
    categoria_id: Mapped[int] = mapped_column(ForeignKey('categorias.id'))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    categoria: Mapped['Categoria'] = relationship(
        'Categoria', back_populates='subcategorias', init=False
    )


@table_registry.mapped_as_dataclass
class Produtos:
    __tablename__ = 'produtos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    sku: Mapped[str] = mapped_column(unique=True)
    nome: Mapped[str] = mapped_column()
    fabricante: Mapped[str] = mapped_column()
    preco: Mapped[float] = mapped_column()
    ativo: Mapped[bool] = mapped_column()
    categoria_id: Mapped[int | None] = mapped_column(
        nullable=True, default=None
    )
    subcategoria_id: Mapped[int | None] = mapped_column(
        nullable=True, default=None
    )
    dimensao: Mapped[str | None] = mapped_column(nullable=True, default=None)
    peso: Mapped[float | None] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    estoque: Mapped[list['Estoque']] = relationship(
        'Estoque', back_populates='produto', init=False
    )


@table_registry.mapped_as_dataclass
class Estoque:
    __tablename__ = 'estoque'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    produto_sku: Mapped[str] = mapped_column(ForeignKey('produtos.sku'))
    fornecedor_id: Mapped[int] = mapped_column(ForeignKey('fornecedores.id'))
    quantidade: Mapped[int] = mapped_column()
    preco_de_aquisicao: Mapped[float] = mapped_column()
    data_de_aquisicao: Mapped[datetime] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    produto: Mapped['Produtos'] = relationship(
        'Produtos', back_populates='estoque', init=False
    )
    fornecedor: Mapped['Fornecedores'] = relationship(
        'Fornecedores', back_populates='estoques', init=False
    )


@table_registry.mapped_as_dataclass
class Fornecedores:
    __tablename__ = 'fornecedores'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column()
    cnpj: Mapped[str] = mapped_column()
    telefone: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    endereco: Mapped[str] = mapped_column()
    cidade: Mapped[str] = mapped_column()
    estado: Mapped[str] = mapped_column()
    pais: Mapped[str] = mapped_column()
    cep: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    ativo: Mapped[bool] = mapped_column(default=True)
    estoques: Mapped[list[Estoque]] = relationship(
        'Estoque', back_populates='fornecedor', init=False
    )
