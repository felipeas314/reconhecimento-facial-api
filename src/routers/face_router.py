from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from qdrant_client import QdrantClient

from src.config.database import get_qdrant_client
from src.repositories.face_repository import FaceRepository
from src.schemas.face import FaceRecognizeResponse, FaceRegisterResponse
from src.services.face_service import FaceService

router = APIRouter(prefix="/faces", tags=["Faces"])


def get_face_service(qdrant: QdrantClient = Depends(get_qdrant_client)) -> FaceService:
    """Dependency injection para FaceService."""
    repository = FaceRepository(qdrant)
    return FaceService(repository)


@router.post("/register", response_model=FaceRegisterResponse)
async def register_face(
    label: str = Form(...),
    File1: Optional[UploadFile] = File(None),
    File2: Optional[UploadFile] = File(None),
    File3: Optional[UploadFile] = File(None),
    service: FaceService = Depends(get_face_service)
):
    """Cadastra uma nova face no sistema."""
    files = [f for f in [File1, File2, File3] if f is not None]

    if len(files) < 3:
        raise HTTPException(
            status_code=400,
            detail="Por favor, envie 3 imagens para o cadastro."
        )

    images_bytes = [await f.read() for f in files]

    if service.register_face(images_bytes, label):
        return FaceRegisterResponse(message="Rosto cadastrado com sucesso.")

    raise HTTPException(status_code=500, detail="Erro ao registrar o rosto.")


@router.post("/recognize", response_model=FaceRecognizeResponse)
async def recognize_face(
    File1: UploadFile = File(...),
    service: FaceService = Depends(get_face_service)
):
    """Reconhece uma face comparando com as cadastradas."""
    image_bytes = await File1.read()
    results = service.recognize_face(image_bytes)

    if not results:
        return FaceRecognizeResponse(message="Nenhuma correspondência encontrada.")

    return FaceRecognizeResponse(result=results)
