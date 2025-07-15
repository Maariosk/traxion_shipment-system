from datetime import datetime
from pydantic import BaseModel
from typing import Literal

ShipmentEventType = Literal["INTEGRATED", "ON_ROUTE", "TRANSPORT_ARRIVAL", "COMPLETED", "REJECTED"]

class ShipmentEvent(BaseModel):
    shipment_id: str
    event: ShipmentEventType
    origin_date: datetime
    author: str
