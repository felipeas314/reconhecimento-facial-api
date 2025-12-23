import os
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from utils.face_utils import register_face, recognize_face
from utils.upload_utils import save_uploaded_files

# Configuração do Qdrant
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "faces"
VECTOR_SIZE = 128  # Tamanho do embedding do face_recognition

qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def init_qdrant():
    """Inicializa a collection do Qdrant se não existir."""
    collections = qdrant.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME not in collection_names:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{COLLECTION_NAME}' criada com sucesso.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_qdrant()
    yield


app = FastAPI(
    title="API de Reconhecimento Facial",
    description="API para cadastro e reconhecimento de faces usando Qdrant",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/post-face")
async def post_face(
    label: str = Form(...),
    File1: Optional[UploadFile] = File(None),
    File2: Optional[UploadFile] = File(None),
    File3: Optional[UploadFile] = File(None),
):
    """Rota para cadastrar rosto."""
    files = [f for f in [File1, File2, File3] if f is not None]

    if len(files) < 3:
        raise HTTPException(status_code=400, detail="Por favor, envie 3 imagens para o cadastro.")

    file_paths = await save_uploaded_files(files, "uploads/")

    result = register_face(file_paths, label, qdrant)
    if result:
        return {"message": "Rosto cadastrado com sucesso."}

    raise HTTPException(status_code=500, detail="Erro ao registrar o rosto.")


@app.post("/check-face")
async def check_face(File1: UploadFile = File(...)):
    """Rota para reconhecer rosto."""
    file_path = await save_uploaded_files([File1], "uploads/", single=True)
    results = recognize_face(file_path, qdrant)

    if not results:
        return {"message": "Nenhuma correspondência encontrada."}

    return {"result": results}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
