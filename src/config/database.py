from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from src.config.settings import get_settings

settings = get_settings()

# Instância global do cliente Qdrant
qdrant_client = QdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port
)


def init_database():
    """Inicializa a collection do Qdrant se não existir."""
    collections = qdrant_client.get_collections().collections
    collection_names = [c.name for c in collections]

    if settings.qdrant_collection_name not in collection_names:
        qdrant_client.create_collection(
            collection_name=settings.qdrant_collection_name,
            vectors_config=VectorParams(
                size=settings.vector_size,
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{settings.qdrant_collection_name}' criada com sucesso.")


def get_qdrant_client() -> QdrantClient:
    """Dependency injection para o cliente Qdrant."""
    return qdrant_client
