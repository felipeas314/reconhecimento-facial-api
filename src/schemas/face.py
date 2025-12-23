from typing import List, Optional
from pydantic import BaseModel


class FaceMatch(BaseModel):
    """DTO para resultado de match de face."""
    label: str
    distance: float


class FaceRegisterResponse(BaseModel):
    """DTO para resposta de cadastro de face."""
    message: str


class FaceRecognizeResponse(BaseModel):
    """DTO para resposta de reconhecimento de face."""
    result: Optional[List[FaceMatch]] = None
    message: Optional[str] = None


class HealthResponse(BaseModel):
    """DTO para resposta de health check."""
    status: str
