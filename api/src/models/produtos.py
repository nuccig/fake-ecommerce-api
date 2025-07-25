from datetime import datetime
from typing import Optional

from pydantic import BaseModel  # type: ignore
from sqlalchemy import (  # type: ignore
    TIMESTAMP,
    Boolean,
    Column,
    Decimal,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship  # type: ignore

from .base import BaseModel as SQLAlchemyBase


# SQLAlchemy Model
class Produto(SQLAlchemyBase):
    __tablename__ = "produtos"

    nome = Column(String(200), nullable=False)
    descricao = Column(Text)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), ondelete="SET NULL")
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), ondelete="SET NULL")
    preco = Column(Decimal(10, 2), nullable=False)
    custo = Column(Decimal(10, 2))
    peso = Column(Decimal(8, 3))
    quantidade_estoque = Column(Integer, default=0)
    em_estoque = Column(Boolean, default=True)
    ativo = Column(Boolean, default=True)
    criado_em = Column(TIMESTAMP, default=func.current_timestamp())

    itens_carrinho = relationship("ItensCarrinho", back_populates="produto")
    itens_venda = relationship("ItensVenda", back_populates="produto")
    fornecedores = relationship("Fornecedor", back_populates="produto")
    categorias = relationship("Categoria", back_populates="produto")

    def __repr__(self):
        return f"<Produto(id={self.id}, nome='{self.nome}', fornecedor_id='{self.fornecedor_id}')>"


# Pydantic Schemas
class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    categoria_id: Optional[int] = None
    fornecedor_id: Optional[int] = None
    preco: float
    custo: Optional[float] = None
    peso: Optional[float] = None
    quantidade_estoque: Optional[int] = 0
    em_estoque: Optional[bool] = True
    ativo: Optional[bool] = True


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(ProdutoBase):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    categoria_id: Optional[int] = None
    fornecedor_id: Optional[int] = None
    preco: Optional[float] = None
    custo: Optional[float] = None
    peso: Optional[float] = None
    quantidade_estoque: Optional[int] = None
    em_estoque: Optional[bool] = None
    ativo: Optional[bool] = None


class ProdutoResponse(ProdutoBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
