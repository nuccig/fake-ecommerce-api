import uvicorn  # type: ignore
from fastapi import FastAPI  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore

from .api.routes.api_router import api_router
from .core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# if __name__ == "__main__":
#     import uvicorn  # type: ignore

#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
