from typing import Optional

from pydantic import BaseModel, validator  # type: ignore
from sqlalchemy import (  # type: ignore
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship  # type: ignore

from .base import BaseModel as SQLAlchemyBase


# SQLAlchemy Model
class Endereco(SQLAlchemyBase):
    __tablename__ = "enderecos"

    cliente_id = Column(
        Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False
    )
    cep = Column(String(10), nullable=False)
    logradouro = Column(String(200), nullable=False)
    numero = Column(String(10), nullable=False)
    complemento = Column(String(100))
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    endereco_principal = Column(Boolean, default=False)
    criado_em = Column(TIMESTAMP, default=func.current_timestamp())

    cliente = relationship("Cliente", back_populates="enderecos")
    vendas = relationship("Venda", back_populates="endereco")

    def __repr__(self):
        return f"<Endereco(id={self.id}, logradouro='{self.logradouro}', numero='{self.numero}', cep='{self.cep}')>"


# Pydantic Schemas
class EnderecoBase(BaseModel):
    cliente_id: int
    cep: str
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: str
    endereco_principal: Optional[bool] = False

    @validator("estado")
    def validate_estado(cls, v):
        if v and len(v) != 2:
            raise ValueError("Estado deve ter 2 caracteres")
        return v.upper() if v else v

    @validator("cep")
    def validate_cep(cls, v):
        if v and len(v.replace(".", "").replace("-", "")) != 8:
            raise ValueError("CEP deve ter 8 dígitos")
        return v


class EnderecoCreate(EnderecoBase):
    pass


class EnderecoUpdate(EnderecoBase):
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None


class EnderecoResponse(EnderecoBase):
    id: int

    class Config:
        from_attributes = True
