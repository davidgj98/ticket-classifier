import pytest
from httpx import AsyncClient


class TestExport:
    @pytest.mark.asyncio
    async def test_export_csv(self, client: AsyncClient):
        response = await client.get("/export/csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers.get("content-type", "")
        assert "filename=tickets.csv" in response.headers.get(
            "content-disposition", ""
        )

    @pytest.mark.asyncio
    async def test_export_json(self, client: AsyncClient):
        response = await client.get("/export/json")
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")
        assert "filename=tickets.json" in response.headers.get(
            "content-disposition", ""
        )
