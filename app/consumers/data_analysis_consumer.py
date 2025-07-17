import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from app.services.message_bus import subscribe

# Cargar variables de entorno
load_dotenv()

# Conexión a MongoDB
mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB", "shipment_system")
client = MongoClient(mongo_uri)
db = client[mongo_db]
summary_collection = db["shipment_summary"]

# Variables de análisis
total_shipments = 0
completed_shipments = 0
rejected_shipments = 0

def handle_event(message: str):
    global total_shipments, completed_shipments, rejected_shipments

    try:
        data = json.loads(message)
        event = data.get("event")

        if event in ["COMPLETED", "REJECTED"]:
            total_shipments += 1
            if event == "COMPLETED":
                completed_shipments += 1
            elif event == "REJECTED":
                rejected_shipments += 1

            print(f"[Data Analysis] Total: {total_shipments}, Completed: {completed_shipments}, Rejected: {rejected_shipments}")

            # Guardar resumen actualizado
            summary_collection.update_one(
                {"_id": "summary"},
                {
                    "$set": {
                        "total_shipments": total_shipments,
                        "completed_shipments": completed_shipments,
                        "rejected_shipments": rejected_shipments
                    }
                },
                upsert=True
            )

    except Exception as e:
        print(f"[ERROR] Failed to process message: {message} — {e}")

if __name__ == "__main__":
    print("[DATA ANALYSIS] Starting consumer...")
    future = subscribe("shipment_events", handle_event)

    if future:
        future.result()
