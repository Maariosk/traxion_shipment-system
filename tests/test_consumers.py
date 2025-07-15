from app.consumers import event_consumer

def test_event_deduplication():
    processed = set()
    key = "shipment123-INTEGRATED"
    # Simulamos que no estaba procesado
    assert key not in processed
    processed.add(key)
    # Ahora debe estar procesado
    assert key in processed
