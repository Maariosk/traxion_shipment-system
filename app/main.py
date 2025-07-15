from fastapi import FastAPI
from app.api import shipments, shipment_events

app = FastAPI(title="Shipment System Event Driven")

app.include_router(shipments.router)
app.include_router(shipment_events.router)