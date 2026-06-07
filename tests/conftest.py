from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.services.ollama import OllamaService


@pytest.fixture
def mock_ollama() -> AsyncMock:
    mock = AsyncMock(spec=OllamaService)

    async def fake_classify(self, text: str, model: str) -> dict[str, str]:
        return {
            "category": "Network",
            "priority": "High",
            "team": "Network Team",
            "summary": "User cannot access Salesforce due to 403 error",
            "confidence": "High",
            "reasoning": "Multiple users affected, service unavailable",
        }

    async def fake_list_models(self) -> list[str]:
        return ["phi4-mini:latest", "qwen2.5:3b"]

    async def fake_check_health(self) -> bool:
        return True

    mock.classify = fake_classify
    mock.list_models = fake_list_models
    mock.check_health = fake_check_health
    return mock


@pytest.fixture
async def client(mock_ollama: AsyncMock) -> AsyncClient:
    with (
        patch.object(OllamaService, "classify", mock_ollama.classify),
        patch.object(OllamaService, "list_models", mock_ollama.list_models),
        patch.object(OllamaService, "check_health", mock_ollama.check_health),
    ):
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            yield ac
