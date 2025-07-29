from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from ...core.database import get_db
from ...models.clientes import Cliente
from ...models.enderecos import (
    Endereco,
    EnderecoCreate,
    EnderecoResponse,
    EnderecoUpdate,
)

router = APIRouter(tags=["Endereços"])


@router.post(
    "/enderecos", response_model=EnderecoResponse, status_code=status.HTTP_201_CREATED
)
async def criar_endereco(endereco: EnderecoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo endereço para um cliente.
    """
    cliente = db.query(Cliente).filter(Cliente.id == endereco.cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )

    db_endereco = Endereco(**endereco.dict())
    db.add(db_endereco)
    db.commit()
    db.refresh(db_endereco)

    return db_endereco


@router.get("/enderecos", response_model=List[EnderecoResponse])
async def listar_enderecos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Lista todos os endereços com paginação.
    """
    enderecos = db.query(Endereco).offset(skip).limit(limit).all()
    return enderecos


@router.get("/enderecos/{endereco_id}", response_model=EnderecoResponse)
async def obter_endereco(endereco_id: int, db: Session = Depends(get_db)):
    """
    Obtém um endereço específico pelo ID.
    """
    endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
    if not endereco:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado"
        )
    return endereco


@router.get("/enderecos/cliente/{cliente_id}", response_model=EnderecoResponse)
async def obter_endereco_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Obtém o endereço de um cliente específico.
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )

    endereco = db.query(Endereco).filter(Endereco.cliente_id == cliente_id).first()
    if not endereco:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endereço não encontrado para este cliente",
        )
    return endereco


@router.delete("/enderecos/{endereco_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_endereco(endereco_id: int, db: Session = Depends(get_db)):
    """
    Deleta um endereço específico pelo ID.
    """
    endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
    if not endereco:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado"
        )

    db.delete(endereco)
    db.commit()


@router.put("/enderecos/{endereco_id}", response_model=EnderecoResponse)
async def atualizar_endereco(
    endereco_id: int, endereco: EnderecoUpdate, db: Session = Depends(get_db)
):
    """
    Atualiza um endereço específico pelo ID.
    """
    db_endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
    if not db_endereco:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado"
        )

    for key, value in endereco.dict(exclude_unset=True).items():
        setattr(db_endereco, key, value)

    db.commit()
    db.refresh(db_endereco)
    return db_endereco


@router.get("/enderecos/buscar")
async def buscar_enderecos(
    cliente_id: Optional[int] = None,
    cep: Optional[str] = None,
    logradouro: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Busca endereços por cliente, CEP ou logradouro.
    """
    query = db.query(Endereco)

    if cliente_id:
        query = query.filter(Endereco.cliente_id == cliente_id)
    if cep:
        query = query.filter(Endereco.cep.ilike(f"%{cep}%"))
    if logradouro:
        query = query.filter(Endereco.logradouro.ilike(f"%{logradouro}%"))

    enderecos = query.all()
    if not enderecos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum endereço encontrado"
        )

    return enderecos
    if cpf:
        query = query.filter(Cliente.cpf == cpf)
    if email:
        query = query.filter(Cliente.email.ilike(f"%{email}%"))

    clientes = query.all()
    if not clientes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum cliente encontrado"
        )

    return clientes
