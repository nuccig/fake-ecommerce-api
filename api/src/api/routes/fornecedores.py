from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from ...core.database import get_db
from ...models.fornecedores import (
    Fornecedor,
    FornecedorCreate,
    FornecedorResponse,
    FornecedorUpdate,
)

router = APIRouter(tags=["Fornecedores"])


@router.post(
    "/fornecedores",
    response_model=FornecedorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def criar_fornecedor(fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    """
    Cria um novo fornecedor.
    """
    fornecedor_existente = (
        db.query(Fornecedor).filter(Fornecedor.cnpj == fornecedor.cnpj).first()
    )
    if fornecedor_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fornecedor com este CNPJ já existe",
        )

    db_fornecedor = Fornecedor(**fornecedor.dict())
    db.add(db_fornecedor)
    db.commit()
    db.refresh(db_fornecedor)

    return db_fornecedor


@router.get("/fornecedores", response_model=List[FornecedorResponse])
async def listar_fornecedores(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Lista todos os fornecedores com paginação.
    """
    fornecedores = db.query(Fornecedor).offset(skip).limit(limit).all()
    return fornecedores


@router.get("/fornecedores/{fornecedor_id}", response_model=FornecedorResponse)
async def obter_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    """
    Obtém um fornecedor específico pelo ID.
    """
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado"
        )
    return fornecedor


@router.put("/fornecedores/{fornecedor_id}", response_model=FornecedorUpdate)
async def atualizar_fornecedor(
    fornecedor_id: int,
    fornecedor_update: FornecedorUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza um cliente específico pelo ID.
    """
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado"
        )

    for key, value in fornecedor_update.dict().items():
        setattr(fornecedor, key, value)

    db.commit()
    db.refresh(fornecedor)
    return fornecedor


@router.delete("/fornecedores/{fornecedor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    """
    Deleta um fornecedor específico pelo ID.
    """
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado"
        )

    db.delete(fornecedor)
    db.commit()


@router.get("/clientes/buscar")
async def buscar_fornecedores(
    nome: Optional[str] = None,
    cnpj: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Busca fornecedores por nome, CNPJ ou email.
    """
    query = db.query(Fornecedor)

    if nome:
        query = query.filter(Fornecedor.nome.ilike(f"%{nome}%"))
    if cnpj:
        query = query.filter(Fornecedor.cnpj == cnpj)
    if email:
        query = query.filter(Fornecedor.email.ilike(f"%{email}%"))

    fornecedores = query.all()
    if not fornecedores:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum fornecedor encontrado"
        )

    return fornecedores
