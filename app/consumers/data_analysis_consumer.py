import json
from app.core.redis_client import r


total_shipments = 0
completed_shipments = 0
rejected_shipments = 0


def data_analysis_consumer():
    pubsub = r.pubsub()
    pubsub.subscribe("shipment_events")
    print("Data Analysis consumer listening...")

    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            event = data["event"]
            global total_shipments, completed_shipments, rejected_shipments
            if event in ["COMPLETED", "REJECTED"]:
                total_shipments += 1
                if event == "COMPLETED":
                    completed_shipments += 1
                else:
                    rejected_shipments += 1

                print(f"[Data Analysis] Total: {total_shipments}, Completed: {completed_shipments}, Rejected: {rejected_shipments}")


if __name__ == "__main__":
    data_analysis_consumer()