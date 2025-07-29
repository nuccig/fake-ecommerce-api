from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from ...core.database import get_db
from ...models.clientes import Cliente, ClienteCreate, ClienteResponse, ClienteUpdate

router = APIRouter(tags=["Clientes"])


@router.post(
    "/clientes", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED
)
async def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """
    Cria um novo cliente.
    """
    cliente_existente = db.query(Cliente).filter(Cliente.cpf == cliente.cpf).first()
    if cliente_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cliente com este CPF já existe",
        )

    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)

    return db_cliente


@router.get("/clientes", response_model=List[ClienteResponse])
async def listar_clientes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Lista todos os clientes com paginação.
    """
    clientes = db.query(Cliente).offset(skip).limit(limit).all()
    return clientes


@router.get("/clientes/{cliente_id}", response_model=ClienteResponse)
async def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Obtém um cliente específico pelo ID.
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )
    return cliente


@router.put("/clientes/{cliente_id}", response_model=ClienteUpdate)
async def atualizar_cliente(
    cliente_id: int, cliente_update: ClienteUpdate, db: Session = Depends(get_db)
):
    """
    Atualiza um cliente específico pelo ID.
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )

    for key, value in cliente_update.dict().items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Deleta um cliente específico pelo ID.
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )

    db.delete(cliente)
    db.commit()


@router.get("/clientes/buscar")
async def buscar_clientes(
    nome: Optional[str] = None,
    cpf: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Busca clientes por nome, CPF ou email.
    """
    query = db.query(Cliente)

    if nome:
        query = query.filter(Cliente.nome.ilike(f"%{nome}%"))
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
