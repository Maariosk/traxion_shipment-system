from fastapi import APIRouter
from app.models.shipment import Shipment
import json
from app.services.message_bus import bus

router = APIRouter()

@router.post("/v1/shipments")
def create_shipment(shipment: Shipment):
    # Publish to Redis
    bus.publish("shipments", shipment.json())
    return {"message": "Shipment creation event published"}
