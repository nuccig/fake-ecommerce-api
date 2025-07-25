from datetime import datetime
from typing import Optional

from pydantic import BaseModel  # type: ignore
from sqlalchemy import (  # type: ignore
    TIMESTAMP,
    Column,
    Decimal,
    ForeignKey,
    Integer,
    func,
)
from sqlalchemy.orm import relationship  # type: ignore

from .base import BaseModel as SQLAlchemyBase


# SQLAlchemy Model
class ItensCarrinho(SQLAlchemyBase):
    __tablename__ = "itens_carrinho"

    carrinho_id = Column(
        Integer, ForeignKey("carrinhos.id"), nullable=False, ondelete="CASCADE"
    )
    produto_id = Column(
        Integer, ForeignKey("produtos.id"), nullable=False, ondelete="CASCADE"
    )
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Decimal(10, 2), nullable=False)
    criado_em = Column(TIMESTAMP, default=func.current_timestamp())

    carrinhos = relationship("Carrinho", back_populates="itens_carrinho")
    produtos = relationship("Produto", back_populates="itens_carrinho")

    def __repr__(self):
        return f"<ItensCarrinho(id={self.id}, cliente_id='{self.cliente_id}')>"


# Pydantic Schemas
class ItensCarrinhoBase(BaseModel):
    categoria_id: int
    produto_id: int
    quantidade: int
    preco_unitario: float


class ItensCarrinhoCreate(ItensCarrinhoBase):
    pass


class ItensCarrinhoUpdate(ItensCarrinhoBase):
    categoria_id: Optional[int] = None
    produto_id: Optional[int] = None
    quantidade: Optional[int] = None
    preco_unitario: Optional[float] = None


class ItensCarrinhoResponse(ItensCarrinhoBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
