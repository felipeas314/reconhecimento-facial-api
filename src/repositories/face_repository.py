import uuid
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from src.config.settings import get_settings
from src.schemas.face import FaceMatch

settings = get_settings()


class FaceRepository:
    """Repository para operações de face no Qdrant."""

    def __init__(self, qdrant: QdrantClient):
        self.qdrant = qdrant
        self.collection_name = settings.qdrant_collection_name

    def save(self, label: str, embeddings: List) -> None:
        """Salva os embeddings de uma face no Qdrant."""
        points = []
        for embedding in embeddings:
            point_id = str(uuid.uuid4())
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding.tolist(),
                    payload={"label": label}
                )
            )

        self.qdrant.upsert(collection_name=self.collection_name, points=points)

    def search(self, embedding: List, limit: int = 1) -> List[FaceMatch]:
        """Busca faces similares no Qdrant usando busca vetorial."""
        results = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=limit,
            score_threshold=1 - settings.similarity_threshold
        )

        return [
            FaceMatch(
                label=hit.payload["label"],
                distance=1 - hit.score
            )
            for hit in results
        ]
