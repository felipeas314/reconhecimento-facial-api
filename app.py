from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.database import init_database
from src.config.settings import get_settings
from src.routers import face_router, health_router, legacy_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicialização e finalização da aplicação."""
    init_database()
    yield


app = FastAPI(
    title=settings.app_name,
    description="API para cadastro e reconhecimento de faces usando Qdrant",
    version=settings.app_version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health_router.router)
app.include_router(face_router.router)
app.include_router(legacy_router.router)  # Compatibilidade com frontend atual


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
