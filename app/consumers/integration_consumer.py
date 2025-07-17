# app/consumers/integration_consumer.py

import json
import os
from pymongo import MongoClient
from app.services.message_bus import subscribe

# Configuración de MongoDB
mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB", "shipment_system")

client = MongoClient(mongo_uri)
db = client[mongo_db_name]
collection = db["shipments"]

def handle_shipment(message: str):
    try:
        data = json.loads(message)
        shipment_id = data.get("id") or data.get("shipment_id", "unknown")
        print(f"[Integration Consumer] Shipment created: {shipment_id}")
        
        # Inserta en MongoDB
        collection.insert_one(data)

    except Exception as e:
        print(f"[ERROR] Failed to process shipment: {message} — {e}")

if __name__ == "__main__":
    print("[INTEGRATION CONSUMER] Starting...")
    future = subscribe("shipments", handle_shipment)
    if future:
        future.result()
