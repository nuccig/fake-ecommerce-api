from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator  # type: ignore
from sqlalchemy import TIMESTAMP, Boolean, Column, String, Text, func  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from .base import BaseModel as SQLAlchemyBase


# SQLAlchemy Model
class Fornecedor(SQLAlchemyBase):
    __tablename__ = "fornecedores"

    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    telefone = Column(String(20))
    cnpj = Column(String(18), unique=True, index=True)
    endereco = Column(Text)
    cidade = Column(String(100))
    estado = Column(String(2))
    cep = Column(String(9))
    ativo = Column(Boolean, default=True)
    criado_em = Column(TIMESTAMP, default=func.current_timestamp())

    produtos = relationship("Produto", back_populates="fornecedor")

    def __repr__(self):
        return f"<Fornecedor(id={self.id}, nome='{self.nome}', cnpj='{self.cnpj}')>"

    @property
    def is_active(self):
        return self.ativo

    def activate(self):
        self.ativo = True

    def deactivate(self):
        self.ativo = False


# Pydantic Schemas
class FornecedorBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    cnpj: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    ativo: bool = True

    @validator("cnpj")
    def validate_cnpj(cls, v):
        if v and len(v.replace(".", "").replace("/", "").replace("-", "")) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos")
        return v

    @validator("estado")
    def validate_estado(cls, v):
        if v and len(v) != 2:
            raise ValueError("Estado deve ter 2 caracteres")
        return v.upper() if v else v

    @validator("cep")
    def validate_cep(cls, v):
        if v:
            cep_clean = v.replace("-", "")
            if len(cep_clean) != 8 or not cep_clean.isdigit():
                raise ValueError("CEP deve ter 8 dígitos")
        return v


class FornecedorCreate(FornecedorBase):
    pass


class FornecedorUpdate(FornecedorBase):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    ativo: Optional[bool] = None


class FornecedorResponse(FornecedorBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
