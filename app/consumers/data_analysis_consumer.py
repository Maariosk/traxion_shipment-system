# app/consumers/data_analysis_consumer.py

import json
from app.services.message_bus import subscribe

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
    except Exception as e:
        print(f"[ERROR] Failed to process message: {message} — {e}")


if __name__ == "__main__":
    print("[DATA ANALYSIS] Starting consumer...")
    subscribe("shipment_events", handle_event)
