# 📄 README.md

## 🚚 Shipment System (Event-Driven)

Este proyecto implementa un sistema de gestión de envíos basado en arquitectura **event-driven**, usando Python, FastAPI y Redis como bus de mensajes simulado.

### ✅ Arquitectura

- **FastAPI** expone dos endpoints para crear shipments y registrar eventos.
- **Redis** actúa como bus de mensajes para desacoplar productores y consumidores.
- **Consumers** escuchan eventos y realizan persistencia simulada y análisis.

### 🗺️ Flujo de eventos

1️⃣ POST `/v1/shipments`: Publica un evento al canal `shipments`.

2️⃣ `integration_consumer`: Escucha `shipments` y procesa creación de shipment.

3️⃣ POST `/v1/shipment-events`: Publica al canal `shipment_events`.

4️⃣ `event_consumer`: Escucha `shipment_events`, deduplica y procesa eventos.

5️⃣ `data_analysis_consumer`: Escucha `shipment_events`, procesa sólo `COMPLETED` y `REJECTED`, y actualiza métricas.

### ⚙️ Estructura

```
app/
├── api/
│   ├── shipments.py
│   └── shipment_events.py
├── consumers/
│   ├── integration_consumer.py
│   ├── event_consumer.py
│   └── data_analysis_consumer.py
├── core/
│   ├── config.py
│   └── redis_client.py
├── models/
│   ├── shipment.py
│   └── shipment_event.py
├── services/
│   └── message_bus.py
└── main.py
```

### 🚀 Instalación

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### ▶️ Ejecutar API

```bash
uvicorn app.main:app --reload
```

### ▶️ Ejecutar Consumers

```bash
python -m app.consumers.integration_consumer
python -m app.consumers.event_consumer
python -m app.consumers.data_analysis_consumer
```

### 🧪 Probar

- Accede a `/docs` para probar endpoints.
- Observa logs de cada consumer.

### 📦 Requerimientos

```
fastapi
uvicorn
redis
pydantic
```

---

¡Listo para correr localmente o subir a la nube (GCP/AWS) y conectar un Redis gestionado! 🚚💨
