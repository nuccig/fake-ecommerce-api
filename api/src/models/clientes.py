from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, validator  # type: ignore
from sqlalchemy import TIMESTAMP, Column, Date, Enum, String, func  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from .base import BaseModel as SQLAlchemyBase


# SQLAlchemy Model
class Cliente(SQLAlchemyBase):
    __tablename__ = "clientes"

    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    telefone = Column(String(20))
    cpf = Column(String(14), unique=True, index=True)
    data_nascimento = Column(Date)
    genero = Column(Enum("M", "F", "Outro"), default="Outro")
    criado_em = Column(TIMESTAMP, default=func.current_timestamp())

    enderecos = relationship("Endereco", back_populates="cliente")
    vendas = relationship("Venda", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(id={self.id}, nome='{self.nome}', cpf='{self.cpf}')>"


# Pydantic Schemas
class ClienteBase(BaseModel):
    nome: str
    sobrenome: str
    email: EmailStr
    telefone: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[date] = None
    genero: Optional[Literal["M", "F", "Outro"]] = None

    @validator("cpf")
    def validate_cpf(cls, v):
        if v and len(v.replace(".", "").replace("/", "").replace("-", "")) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        return v

    @validator("data_nascimento")
    def validate_data_nascimento(cls, v):
        if v and v > date.today():
            raise ValueError("Data de nascimento não pode ser no futuro")
        return v


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(ClienteBase):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    genero: Optional[List[Literal["M", "F", "Outro"]]] = None


class ClienteResponse(ClienteBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
