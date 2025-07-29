from typing import List

from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from ...core.database import get_db
from ...models.categorias import (
    Categoria,
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate,
)

router = APIRouter(tags=["Categorias"])


@router.post(
    "/categorias", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED
)
async def criar_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova categoria.
    """

    db_categoria = Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)

    return db_categoria


@router.get("/categorias", response_model=List[CategoriaResponse])
async def listar_categorias(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Lista todas as categorias com paginação.
    """
    categorias = db.query(Categoria).offset(skip).limit(limit).all()
    return categorias


@router.get("/categorias/{categoria_id}", response_model=CategoriaResponse)
async def obter_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """
    Obtém uma categoria específica pelo ID.
    """
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not Categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrado"
        )
    return categoria

@router.delete("/categorias/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma categoria específica pelo ID.
    """
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada"
        )

    db.delete(categoria)
    db.commit()
    
@router.patch("/categorias/{categoria_id}", status_code=status.HTTP_200_OK)
async def atualizar_categoria(categoria_id: int, categoria_update: CategoriaUpdate, db: Session = Depends(get_db)):
    """
    Atualiza uma categoria específica pelo ID
    """
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada"
        )

    # Atualiza os campos da categoria com os dados fornecidos
    for key, value in categoria_update.dict(exclude_unset=True).items():
        setattr(categoria, key, value)

    db.commit()
    db.refresh(categoria)
    return categoria