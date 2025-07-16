# app/consumers/integration_consumer.py

import json
from app.services.message_bus import subscribe

def handle_shipment(message: str):
    try:
        data = json.loads(message)
        print(f"[Integration Consumer] Shipment created: {data['id']}")
        # Aquí puedes simular persistencia en base de datos, archivo, etc.
    except Exception as e:
        print(f"[ERROR] Failed to process shipment: {message} — {e}")


if __name__ == "__main__":
    print("[INTEGRATION CONSUMER] Starting...")
    future = subscribe("shipments", handle_shipment)
    future.result()  # Esto bloquea el hilo y mantiene el proceso corriendo

