from fastapi import APIRouter

from app.config import get_settings
from app.services.ollama import OllamaService

router = APIRouter(tags=["models"])
ollama_service = OllamaService()


@router.get("/models")
async def list_models() -> dict[str, list[str]]:
    settings = get_settings()
    models = await ollama_service.list_models()
    if not models:
        models = [settings.default_model]
    return {"models": sorted(models)}
