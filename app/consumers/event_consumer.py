import json
from app.core.redis_client import r

processed_events = set()


def event_consumer():
    pubsub = r.pubsub()
    pubsub.subscribe("shipment_events")
    print("Event consumer listening...")

    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            key = f"{data['shipment_id']}-{data['event']}"
            if key not in processed_events:
                processed_events.add(key)
                print(f"[Event Consumer] New event for shipment {data['shipment_id']}: {data['event']}")
                # Simulate persistence
            else:
                print(f"[Event Consumer] Duplicate event ignored: {key}")


if __name__ == "__main__":
    event_consumer()