import json
from app.core.redis_client import r


def integration_consumer():
    pubsub = r.pubsub()
    pubsub.subscribe("shipments")
    print("Integration consumer listening...")

    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            print(f"[Integration Consumer] Shipment created: {data['id']}")
            # Simulate persistence


if __name__ == "__main__":
    integration_consumer()