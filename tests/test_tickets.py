import pytest
from httpx import AsyncClient


class TestTickets:
    @pytest.mark.asyncio
    async def test_create_ticket(self, client: AsyncClient):
        response = await client.post(
            "/tickets",
            json={
                "text": "User cannot access Salesforce",
                "category": "Network",
                "priority": "High",
                "team": "Network Team",
                "summary": "Access issue",
                "confidence": "High",
                "reasoning": "Test",
                "model": "phi4-mini:latest",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["ticket_number"].startswith("TCK-")
        assert data["status"] == "Open"
        assert data["category"] == "Network"

    @pytest.mark.asyncio
    async def test_list_tickets(self, client: AsyncClient):
        response = await client.get("/tickets")
        assert response.status_code == 200
        data = response.json()
        assert "tickets" in data
        assert "total" in data

    @pytest.mark.asyncio
    async def test_create_and_get_ticket(self, client: AsyncClient):
        create_res = await client.post(
            "/tickets",
            json={
                "text": "Database slow",
                "category": "Database",
                "priority": "Critical",
                "team": "DBA Team",
                "summary": "DB slow",
                "confidence": "High",
                "reasoning": "Test",
                "model": "phi4-mini:latest",
            },
        )
        ticket_id = create_res.json()["id"]

        get_res = await client.get(f"/tickets/{ticket_id}")
        assert get_res.status_code == 200
        assert get_res.json()["category"] == "Database"

    @pytest.mark.asyncio
    async def test_update_status(self, client: AsyncClient):
        create_res = await client.post(
            "/tickets",
            json={
                "text": "Server down",
                "category": "Infrastructure",
                "priority": "Critical",
                "team": "General IT",
                "summary": "Server down",
                "confidence": "High",
                "reasoning": "Test",
                "model": "phi4-mini:latest",
            },
        )
        ticket_id = create_res.json()["id"]

        patch_res = await client.patch(
            f"/tickets/{ticket_id}/status",
            json={"status": "In Progress"},
        )
        assert patch_res.status_code == 200
        assert patch_res.json()["status"] == "In Progress"

    @pytest.mark.asyncio
    async def test_update_status_invalid(self, client: AsyncClient):
        create_res = await client.post(
            "/tickets",
            json={
                "text": "Email issue",
                "category": "Email",
                "priority": "Medium",
                "team": "Email Team",
                "summary": "Email issue",
                "confidence": "Medium",
                "reasoning": "Test",
                "model": "phi4-mini:latest",
            },
        )
        ticket_id = create_res.json()["id"]

        patch_res = await client.patch(
            f"/tickets/{ticket_id}/status",
            json={"status": "Invalid"},
        )
        assert patch_res.status_code == 422

    @pytest.mark.asyncio
    async def test_delete_ticket(self, client: AsyncClient):
        create_res = await client.post(
            "/tickets",
            json={
                "text": "Test delete",
                "category": "Other",
                "priority": "Low",
                "team": "General IT",
                "summary": "Test",
                "confidence": "Low",
                "reasoning": "Test",
                "model": "phi4-mini:latest",
            },
        )
        ticket_id = create_res.json()["id"]

        del_res = await client.delete(f"/tickets/{ticket_id}")
        assert del_res.status_code == 200

        get_res = await client.get(f"/tickets/{ticket_id}")
        assert get_res.status_code == 404

    @pytest.mark.asyncio
    async def test_not_found(self, client: AsyncClient):
        response = await client.get("/tickets/99999")
        assert response.status_code == 404
