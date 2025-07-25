from datetime import datetime

from pydantic import BaseModel  # type: ignore
from sqlalchemy import (  # type: ignore
    TIMESTAMP,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    func,
)
from sqlalchemy.orm import relationship  # type: ignore

from .base import BaseModel as SQLAlchemyBase


# SQLAlchemy Model
class Carrinho(SQLAlchemyBase):
    __tablename__ = "carrinhos"

    cliente_id = Column(
        Integer, ForeignKey("clientes.id"), nullable=False, ondelete="CASCADE"
    )
    criado_em = Column(TIMESTAMP, default=func.current_timestamp())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    clientes = relationship("Cliente", back_populates="carrinhos")
    itens_carrinhos = relationship("ItensCarrinho", back_populates="carrinho")

    def __repr__(self):
        return f"<Carrinho(id={self.id}, cliente_id={self.cliente_id})>"


# Pydantic Schemas
class CarrinhoBase(BaseModel):
    cliente_id: int


class CarrinhoCreate(CarrinhoBase):
    pass


class CarrinhoResponse(CarrinhoBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
