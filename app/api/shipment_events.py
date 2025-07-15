from fastapi import APIRouter
from app.models.shipment_event import ShipmentEvent
import json
from app.services.message_bus import bus

router = APIRouter()

@router.post("/v1/shipment-events")
def create_shipment_event(event: ShipmentEvent):
    bus.publish("shipment_events", event.model_dump_json())
    return {"message": "Shipment event published"}
