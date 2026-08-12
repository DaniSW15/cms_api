from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version="0.1.0",
)


# Montar carpeta uploads como archivos estáticos
# Ahora podrás ver imágenes en: http://localhost:8000/uploads/nombre.jpg
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


# Incluye TODOS los routers de v1 bajo el prefijo /api/v1
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health():
    """
    Endpoint para verificar que la API está viva.
    Útil para monitoreo y para saber si Docker/PostgreSQL están funcionando correctamente.
    """
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "debug": settings.DEBUG,
    }
