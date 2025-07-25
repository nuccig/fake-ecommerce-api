from datetime import datetime
from typing import Optional

from pydantic import BaseModel  # type: ignore
from sqlalchemy import Column, Decimal, ForeignKey, Integer  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from .base import BaseModel as SQLAlchemyBase


# SQLAlchemy Model
class ItensVendas(SQLAlchemyBase):
    __tablename__ = "itens_vendas"

    venda_id = Column(
        Integer, ForeignKey("vendas.id"), nullable=False, ondelete="CASCADE"
    )
    produto_id = Column(
        Integer, ForeignKey("produtos.id"), nullable=False, ondelete="CASCADE"
    )
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Decimal(10, 2), nullable=False)
    subtotal = Column(Decimal(10, 2), nullable=False)

    carrinhos = relationship("Carrinho", back_populates="itens_vendas")
    produtos = relationship("Produto", back_populates="itens_vendas")

    def __repr__(self):
        return f"<ItensVendas(id={self.id}, cliente_id='{self.cliente_id}')>"


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


class ItensVendasResponse(ItensVendasBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
