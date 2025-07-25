from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, validator  # type: ignore
from sqlalchemy import (  # type: ignore
    TIMESTAMP,
    Column,
    Date,
    Decimal,
    Enum,
    ForeignKey,
    Integer,
    func,
)
from sqlalchemy.orm import relationship  # type: ignore

from .base import BaseModel as SQLAlchemyBase


# SQLAlchemy Model
class Venda(SQLAlchemyBase):
    __tablename__ = "vendas"

    cliente_id = Column(
        Integer, ForeignKey("clientes.id"), nullable=False, ondelete="CASCADE"
    )
    endereco_entrega_id = Column(
        Integer, ForeignKey("enderecos.id"), nullable=True, ondelete="SET NULL"
    )
    status = Column(
        Enum("Pendente", "Confirmado", "Enviado", "Entregue", "Cancelado"),
        nullable=False,
        default="Pendente",
    )
    subtotal = Column(Decimal(10, 2), nullable=False)
    frete = Column(Decimal(10, 2), nullable=False, default=0.00)
    total = Column(Decimal(10, 2), nullable=False)
    metodo_pagamento = Column(
        Enum("Cartao_Credito", "Cartao_Debito", "PIX", "Boleto"), nullable=False
    )
    status_pagamento = Column(
        Enum("Pendente", "Aprovado", "Recusado"), nullable=False, default="Pendente"
    )
    data_venda = Column(TIMESTAMP, default=func.current_timestamp())
    data_entrega_prevista = Column(Date, nullable=True)

    clientes = relationship("Cliente", back_populates="vendas")
    enderecos = relationship("Endereco", back_populates="vendas")
    itens_vendas = relationship("ItensVendas", back_populates="venda")

    def __repr__(self):
        return f"<Venda(id={self.id}, cliente_id={self.cliente_id}, status='{self.status}')>"


# Pydantic Schemas
class VendaBase(BaseModel):
    cliente_id: int
    endereco_entrega_id: Optional[int] = None
    status: Literal["Pendente", "Confirmado", "Enviado", "Entregue", "Cancelado"]
    subtotal: float
    frete: float
    total: float
    metodo_pagamento: Literal["Cartao_Credito", "Cartao_Debito", "PIX", "Boleto"]
    status_pagamento: Literal["Pendente", "Aprovado", "Recusado"]
    data_venda: datetime
    data_entrega_prevista: Optional[date] = None


class VendaCreate(VendaBase):
    pass


class VendaUpdate(VendaBase):
    endereco_entrega_id: Optional[int] = None
    status: Optional[
        Literal["Pendente", "Confirmado", "Enviado", "Entregue", "Cancelado"]
    ] = None
    subtotal: Optional[float] = None
    frete: Optional[float] = None
    total: Optional[float] = None
    metodo_pagamento: Optional[
        Literal["Cartao_Credito", "Cartao_Debito", "PIX", "Boleto"]
    ] = None
    status_pagamento: Optional[Literal["Pendente", "Aprovado", "Recusado"]] = None
    data_entrega_prevista: Optional[date] = None


class VendaResponse(VendaBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
