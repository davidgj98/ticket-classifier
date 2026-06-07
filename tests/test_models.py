import pytest
from httpx import AsyncClient


class TestModels:
    @pytest.mark.asyncio
    async def test_list_models(self, client: AsyncClient):
        response = await client.get("/models")
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert "phi4-mini:latest" in data["models"]
        assert "qwen2.5:3b" in data["models"]
