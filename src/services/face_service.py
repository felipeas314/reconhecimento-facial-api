from typing import List

import face_recognition

from src.repositories.face_repository import FaceRepository
from src.schemas.face import FaceMatch


class FaceService:
    """Service para lógica de negócio de reconhecimento facial."""

    def __init__(self, repository: FaceRepository):
        self.repository = repository

    def register_face(self, image_paths: List[str], label: str) -> bool:
        """Registra uma face extraindo embeddings de múltiplas imagens."""
        try:
            embeddings = []
            for path in image_paths:
                image = face_recognition.load_image_file(path)
                face_encodings = face_recognition.face_encodings(image)
                if face_encodings:
                    embeddings.append(face_encodings[0])

            if embeddings:
                self.repository.save(label, embeddings)
                return True

        except Exception as e:
            print(f"Erro ao registrar rosto: {e}")

        return False

    def recognize_face(self, image_path: str) -> List[FaceMatch]:
        """Reconhece faces em uma imagem usando busca vetorial."""
        try:
            image = face_recognition.load_image_file(image_path)
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
