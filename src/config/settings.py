import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação."""

    # App
    app_name: str = "API de Reconhecimento Facial"
    app_version: str = "1.0.0"
    debug: bool = True

    # Qdrant
    qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port: int = int(os.getenv("QDRANT_PORT", "6333"))
    qdrant_collection_name: str = "faces"

    # Face Recognition
    vector_size: int = 128  # Tamanho do embedding do face_recognition
    similarity_threshold: float = 0.6

    # Upload
    upload_dir: str = "uploads"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Retorna instância cacheada das configurações."""
    return Settings()
