from fastapi import APIRouter  # type: ignore

from .categorias import router as categorias_router
from .clientes import router as clientes_router
from .enderecos import router as enderecos_router
from .fornecedores import router as fornecedores_router
from .health import router as health_router
from .produtos import router as produtos_router
from .vendas import router as vendas_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/ecomm/v1")
api_router.include_router(categorias_router, prefix="/ecomm/v1")
api_router.include_router(clientes_router, prefix="/ecomm/v1")
api_router.include_router(enderecos_router, prefix="/ecomm/v1")
api_router.include_router(fornecedores_router, prefix="/ecomm/v1")
api_router.include_router(produtos_router, prefix="/ecomm/v1")
api_router.include_router(vendas_router, prefix="/ecomm/v1")
