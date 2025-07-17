# app/consumers/event_consumer.py

import os
import json
from dotenv import load_dotenv
from app.services.message_bus import subscribe
from pymongo import MongoClient

# Cargar variables de entorno
load_dotenv()

# Conectar a MongoDB
mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB", "shipment_system")
client = MongoClient(mongo_uri)
db = client[mongo_db]
events_collection = db["shipment_events"]

processed_events = set()

def handle_event(message: str):
    try:
        data = json.loads(message)
        key = f"{data['shipment_id']}-{data['event']}"

        if key not in processed_events:
            processed_events.add(key)
            print(f"[Event Consumer] New event for shipment {data['shipment_id']}: {data['event']}")

            # Persistir en MongoDB
            print(f"[DEBUG] Guardando en MongoDB: {data}")
            events_collection.insert_one(data)

        else:
            print(f"[Event Consumer] Duplicate event ignored: {key}")

    except Exception as e:
        print(f"[ERROR] Failed to process message: {message} — {e}")

if __name__ == "__main__":
    print("[EVENT CONSUMER] Starting...")
    future = subscribe("shipment_events", handle_event)

    if future:
        future.result()
