import os

from dotenv import load_dotenv  # type: ignore
from pydantic_settings import BaseSettings  # type: ignore

load_dotenv(".env")


class Settings(BaseSettings):
    """
    Configurações da aplicação Fake Ecommerce API.
    """

    APP_NAME: str = "Fake E-commerce API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    DB_HOST: str = (
        "terraform-20250724042256770800000002.csdsw6cyc9qd.us-east-1.rds.amazonaws.com"
    )
    DB_PORT: int = 3306
    DB_NAME: str = "ecommerce"
    DB_USER: str = os.getenv("DB_USER", "user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")

    API_PREFIX: str = "/api/v1"

    @property
    def DB_URL(self) -> str:
        """Constrói a URL de conexão para MySQL usando PyMySQL."""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
