from datetime import datetime
from pydantic import BaseModel

class Shipment(BaseModel):
    id: str
    origin_date: datetime
    item_amount: int
