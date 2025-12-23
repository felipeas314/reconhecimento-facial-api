import face_recognition
from qdrant_client import QdrantClient
from models.embeddings import save_embedding, search_embedding


def register_face(image_paths: list, label: str, qdrant: QdrantClient):
    """Registra uma face extraindo embeddings de múltiplas imagens."""
    try:
        embeddings = []
        for path in image_paths:
            image = face_recognition.load_image_file(path)
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                embeddings.append(face_encodings[0])

        if embeddings:
            save_embedding(label, embeddings, qdrant)
            return True
    except Exception as e:
        print(f"Erro ao registrar rosto: {e}")
    return False


def recognize_face(image_path: str, qdrant: QdrantClient):
    """Reconhece faces em uma imagem usando busca vetorial no Qdrant."""
    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if not face_encodings:
            return []

        results = []
        for encoding in face_encodings:
            matches = search_embedding(encoding.tolist(), qdrant)
            results.extend(matches)

        return results
    except Exception as e:
        print(f"Erro ao reconhecer rosto: {e}")
    return []
