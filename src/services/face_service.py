from io import BytesIO
from typing import List

import face_recognition
import numpy as np
from PIL import Image

from src.repositories.face_repository import FaceRepository
from src.schemas.face import FaceMatch


class FaceService:
    """Service para lógica de negócio de reconhecimento facial."""

    def __init__(self, repository: FaceRepository):
        self.repository = repository

    def _load_image_from_bytes(self, image_bytes: bytes) -> np.ndarray:
        """Carrega imagem dos bytes para numpy array."""
        image = Image.open(BytesIO(image_bytes))
        return np.array(image)

    def register_face(self, images_bytes: List[bytes], label: str) -> bool:
        """Registra uma face extraindo embeddings de múltiplas imagens."""
        try:
            embeddings = []
            for img_bytes in images_bytes:
                image = self._load_image_from_bytes(img_bytes)
                face_encodings = face_recognition.face_encodings(image)
                if face_encodings:
                    embeddings.append(face_encodings[0])

            if embeddings:
                self.repository.save(label, embeddings)
                return True

        except Exception as e:
            print(f"Erro ao registrar rosto: {e}")

        return False

    def recognize_face(self, image_bytes: bytes) -> List[FaceMatch]:
        """Reconhece faces em uma imagem usando busca vetorial."""
        try:
            image = self._load_image_from_bytes(image_bytes)
            face_encodings = face_recognition.face_encodings(image)

            if not face_encodings:
                return []

            results = []
            for encoding in face_encodings:
                matches = self.repository.search(encoding.tolist())
                results.extend(matches)

            return results

        except Exception as e:
            print(f"Erro ao reconhecer rosto: {e}")

        return []
