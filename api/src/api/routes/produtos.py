from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from ...core.database import get_db
from ...models.produtos import Produto, ProdutoCreate, ProdutoResponse, ProdutoUpdate

router = APIRouter(tags=["Produtos"])


@router.post(
    "/produtos", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED
)
async def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo produto.
    """
    db_produto = Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)

    return db_produto


@router.get("/produtos", response_model=List[ProdutoResponse])
async def listar_produtos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Lista todos os produtos com paginação.
    """
    produtos = db.query(Produto).offset(skip).limit(limit).all()
    return produtos


@router.get("/produtos/{produto_id}", response_model=ProdutoResponse)
async def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    """
    Obtém um produto específico pelo ID.
    """
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )
    return produto


@router.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    """
    Deleta um produto específico pelo ID.
    """
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    db.delete(produto)
    db.commit()


@router.put("/produtos/{produto_id}", response_model=ProdutoResponse)
async def atualizar_produto(
    produto_id: int, produto: ProdutoUpdate, db: Session = Depends(get_db)
):
    """
    Atualiza um produto específico pelo ID.
    """
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    for key, value in produto.dict(exclude_unset=True).items():
        setattr(db_produto, key, value)

    db.commit()
    db.refresh(db_produto)
    return db_produto


@router.get("/produtos/buscar")
async def buscar_produtos(
    nome: Optional[str] = None,
    categoria: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Busca endereços por cliente, CEP ou logradouro.
    """
    query = db.query(Produto)

    if nome:
        query = query.filter(Produto.nome.ilike(f"%{nome}%"))
    if categoria:
        query = query.filter(Produto.categoria.ilike(f"%{categoria}%"))

    produtos = query.all()
    if not produtos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto encontrado"
        )

    return produtos
