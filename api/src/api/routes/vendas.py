from typing import List

from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from ...core.database import get_db
from ...models.clientes import Cliente
from ...models.itens_venda import ItensVendas, ItensVendasCreate
from ...models.vendas import Venda, VendaCreate, VendaResponse

router = APIRouter(tags=["Vendas"])


@router.post(
    "/vendas", response_model=VendaResponse, status_code=status.HTTP_201_CREATED
)
async def criar_venda(venda: VendaCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova venda.
    """
    cliente = db.query(Cliente).filter(Cliente.id == venda.cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )

    db_venda = Venda(**venda.dict())
    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)

    return db_venda


@router.get("/vendas", response_model=List[VendaResponse])
async def listar_vendas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todas as vendas com paginação.
    """
    vendas = db.query(Venda).offset(skip).limit(limit).all()
    return vendas


@router.get("/vendas/{venda_id}", response_model=VendaResponse)
async def obter_venda(venda_id: int, db: Session = Depends(get_db)):
    """
    Obtém uma venda específica pelo ID.
    """
    venda = db.query(Venda).filter(Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Venda não encontrada"
        )
    return venda


@router.get("/vendas/cliente/{cliente_id}", response_model=List[VendaResponse])
async def obter_venda_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Obtém a venda de um cliente específico.
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )

    vendas = db.query(Venda).filter(Venda.cliente_id == cliente_id).all()
    if not vendas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendas não encontradas para este cliente",
        )
    return vendas


@router.delete("/vendas/{venda_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_venda(venda_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma venda específica pelo ID.
    Os itens da venda serão deletados automaticamente devido ao CASCADE.
    """
    venda = db.query(Venda).filter(Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Venda não encontrada"
        )

    db.delete(venda)
    db.commit()


@router.delete("/vendas/cliente/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_venda_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Deleta a venda de um cliente específico.
    """
    # Verifica se o cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )

    venda = db.query(Venda).filter(Venda.cliente_id == cliente_id).first()
    if not venda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venda não encontrada para este cliente",
        )

    db.delete(venda)
    db.commit()


@router.get("/vendas/{venda_id}/itens")
async def obter_itens_venda(venda_id: int, db: Session = Depends(get_db)):
    """
    Obtém todos os itens de uma venda específica.
    """
    # Verifica se a venda existe
    venda = db.query(Venda).filter(Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Venda não encontrada"
        )

    itens = db.query(ItensVendas).filter(ItensVendas.venda_id == venda_id).all()
    return itens


@router.post("/vendas/{venda_id}/itens")
async def adicionar_item_venda(
    venda_id: int, item: ItensVendasCreate, db: Session = Depends(get_db)
):
    """
    Adiciona um item à venda.
    """
    venda = db.query(Venda).filter(Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Venda não encontrada"
        )

    novo_item = ItensVendas(**item.dict(), venda_id=venda_id)
    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)
    return novo_item


@router.delete("/vendas/{venda_id}/itens/{item_id}")
async def remover_item_venda(
    venda_id: int, item_id: int, db: Session = Depends(get_db)
):
    """
    Remove um item específico da venda.
    """
    item = (
        db.query(ItensVendas)
        .filter(ItensVendas.id == item_id, ItensVendas.venda_id == venda_id)
        .first()
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado na venda",
        )

    db.delete(item)
    db.commit()
    return {"detail": "Item removido com sucesso"}
