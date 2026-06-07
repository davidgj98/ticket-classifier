import pytest
from httpx import AsyncClient


class TestHealth:
    @pytest.mark.asyncio
    async def test_health_ok(self, client: AsyncClient):
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["ollama"] == "connected"

    @pytest.mark.asyncio
    async def test_health_root(self, client: AsyncClient):
        response = await client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
