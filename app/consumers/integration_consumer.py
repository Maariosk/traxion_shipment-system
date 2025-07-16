# app/consumers/integration_consumer.py

import json
from app.services.message_bus import subscribe

def handle_shipment(message: str):
    try:
        data = json.loads(message)
        shipment_id = data.get("id") or data.get("shipment_id", "unknown")
        print(f"[Integration Consumer] Shipment created: {shipment_id}")
        # Aquí puedes simular persistencia en base de datos, archivo, etc.
    except Exception as e:
        print(f"[ERROR] Failed to process shipment: {message} — {e}")

if __name__ == "__main__":
    print("[INTEGRATION CONSUMER] Starting...")
    future = subscribe("shipments", handle_shipment)

    # Mantener el proceso vivo en Pub/Sub (para Redis no es necesario pero no afecta)
    if future:
        future.result()
