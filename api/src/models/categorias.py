from datetime import datetime
from typing import Optional

from pydantic import BaseModel  # type: ignore
from sqlalchemy import TIMESTAMP, Boolean, Column, String, Text, func  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from .base import BaseModel as SQLAlchemyBase


# SQLAlchemy Model
class Categoria(SQLAlchemyBase):
    __tablename__ = "categorias"

    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=False)
    ativa = Column(Boolean, default=True)
    criado_em = Column(TIMESTAMP, default=func.current_timestamp())

    produtos = relationship("Produto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(id={self.id}, nome='{self.nome}')>"

    @property
    def is_active(self):
        return self.ativa

    def activate(self):
        self.ativa = True

    def deactivate(self):
        self.ativa = False


# Pydantic Schemas
class CategoriaBase(BaseModel):
    nome: str
    descricao: str
    ativa: bool = True


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    descricao: Optional[str] = None
    ativa: Optional[bool] = None


class CategoriaResponse(CategoriaBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
