# app/consumers/event_consumer.py

import json
from app.services.message_bus import subscribe

processed_events = set()

def handle_event(message: str):
    try:
        data = json.loads(message)
        key = f"{data['shipment_id']}-{data['event']}"

        if key not in processed_events:
            processed_events.add(key)
            print(f"[Event Consumer] New event for shipment {data['shipment_id']}: {data['event']}")
            # Aquí simulas la persistencia real
        else:
            print(f"[Event Consumer] Duplicate event ignored: {key}")

    except Exception as e:
        print(f"[ERROR] Failed to process message: {message} — {e}")


if __name__ == "__main__":
    print("[EVENT CONSUMER] Starting...")
    future = subscribe("shipment_events", handle_event)

    # En caso de Pub/Sub, se requiere .result() para mantenerlo activo
    if future:
        future.result()
