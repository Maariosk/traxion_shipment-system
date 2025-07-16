from app.services.message_bus import subscribe

def handle_debug(msg):
    print(f"[DEBUG] Mensaje recibido: {msg}")

if __name__ == "__main__":
    print("[DEBUG CONSUMER] Escuchando shipment_events...")
    future = subscribe("shipment_events", handle_debug, subscription_name="sub-shipment_events")
    future.result()
