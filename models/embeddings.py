import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


def save_embedding(label: str, embeddings: list, qdrant: QdrantClient, collection_name: str = "faces"):
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

    qdrant.upsert(collection_name=collection_name, points=points)


def search_embedding(embedding: list, qdrant: QdrantClient, collection_name: str = "faces", limit: int = 1, threshold: float = 0.6):
    """Busca faces similares no Qdrant usando busca vetorial."""
    results = qdrant.search(
        collection_name=collection_name,
        query_vector=embedding,
        limit=limit,
        score_threshold=1 - threshold  # Qdrant usa similaridade, convertemos de distância
    )

    return [
        {
            "label": hit.payload["label"],
            "distance": 1 - hit.score  # Convertendo score de volta para distância
        }
        for hit in results
    ]
