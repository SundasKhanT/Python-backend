from backend.config import BASE_URL
import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.tests.test_data_input import test_input


@pytest.mark.asyncio
async def test_ingest_items_rejects_invalid_premium_item():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        response = await ac.post("/api/v1/items/ingest", json=test_input)

    data = response.json()
    print("Response JSON:", data)

    assert response.status_code == 200

    assert any(
        err["name"] == "Mega Widget" and "must have value >= 100" in err["error"]
        for err in data["errors"]
    )

    success_names = [item["name"] for item in data["success"]]
    assert "Basic Widget" in success_names
    assert "Gold Service" in success_names
