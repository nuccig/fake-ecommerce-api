from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from .config import settings

engine = create_engine(settings.DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Cria uma sessão de banco de dados para cada requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
