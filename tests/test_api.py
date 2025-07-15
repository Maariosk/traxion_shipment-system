import pytest
from httpx import AsyncClient
from app.main import app
from datetime import datetime

@pytest.mark.asyncio
async def test_create_shipment():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "id": "test-123",
            "origin_date": datetime.now().isoformat(),
            "item_amount": 5
        }
        response = await ac.post("/v1/shipments", json=payload)
        assert response.status_code == 200
        assert response.json()["message"] == "Shipment creation event published"

@pytest.mark.asyncio
async def test_create_shipment_event():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "shipment_id": "test-123",
            "event": "INTEGRATED",
            "origin_date": datetime.now().isoformat(),
            "author": "tester"
        }
        response = await ac.post("/v1/shipment-events", json=payload)
        assert response.status_code == 200
        assert response.json()["message"] == "Shipment event published"
