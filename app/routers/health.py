from fastapi import APIRouter

from app.services.ollama import OllamaService

router = APIRouter(tags=["health"])
ollama_service = OllamaService()


@router.get("/health")
async def health() -> dict[str, str]:
    connected = await ollama_service.check_health()
    if connected:
        return {"status": "ok", "ollama": "connected"}
    return {"status": "degraded", "ollama": "disconnected"}
