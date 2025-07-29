from datetime import datetime
from typing import Optional

from pydantic import BaseModel  # type: ignore
from sqlalchemy import Column, ForeignKey, Integer, Numeric  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from .base import BaseModel as SQLAlchemyBase


# SQLAlchemy Model
class ItensVendas(SQLAlchemyBase):
    __tablename__ = "itens_venda"

    venda_id = Column(
        Integer, ForeignKey("vendas.id", ondelete="CASCADE"), nullable=False
    )
    produto_id = Column(
        Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False
    )
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    venda = relationship("Venda", back_populates="itens_venda")
    produto = relationship("Produto", back_populates="itens_venda")

    def __repr__(self):
        return f"<ItensVendas(id={self.id}, venda_id={self.venda_id}, produto_id={self.produto_id})>"  # Corrigir cliente_id


# Pydantic Schemas
class ItensVendasBase(BaseModel):
    venda_id: int
    produto_id: int
    quantidade: int
    preco_unitario: float
    subtotal: float


class ItensVendasCreate(ItensVendasBase):
    pass


class ItensVendasUpdate(ItensVendasBase):
    produto_id: Optional[int] = None
    quantidade: Optional[int] = None
    subtotal: Optional[float] = None
