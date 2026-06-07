import pytest
from httpx import AsyncClient


class TestClassify:
    @pytest.mark.asyncio
    async def test_classify_valid(self, client: AsyncClient):
        response = await client.post(
            "/classify",
            json={"text": "User cannot access Salesforce, getting 403 error"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "Network"
        assert data["priority"] == "High"
        assert data["team"] == "Network Team"
        assert data["confidence"] == "High"

    @pytest.mark.asyncio
    async def test_classify_empty_text(self, client: AsyncClient):
        response = await client.post(
            "/classify",
            json={"text": "   ", "model": "phi4-mini:latest"},
        )
        assert response.status_code == 400
        data = response.json()
        assert "empty" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_classify_custom_model(self, client: AsyncClient):
        response = await client.post(
            "/classify",
            json={"text": "Server is down", "model": "phi4-mini:latest"},
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_classify_invalid_json(self, client: AsyncClient):
        response = await client.post(
            "/classify",
            json={"not_text": "something"},
        )
        assert response.status_code == 422
