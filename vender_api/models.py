from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Produtos:
    __tablename__ = 'produtos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    sku: Mapped[str] = mapped_column(unique=True)
    nome: Mapped[str] = mapped_column()
    fabricante: Mapped[str] = mapped_column()
    id_fabricante: Mapped[str] = mapped_column()
    categoria: Mapped[str] = mapped_column()
    peso: Mapped[float] = mapped_column()
    dimensao: Mapped[str] = mapped_column()
    ativo: Mapped[bool] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
