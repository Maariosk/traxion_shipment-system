# 📄 README.md

## 🚚 Shipment System (Event-Driven)

Este proyecto implementa un sistema de gestión de envíos basado en arquitectura **event-driven**, usando Python, FastAPI y un bus de mensajes configurable entre **Redis** y **Google Cloud Pub/Sub**. Además, integra **MongoDB Atlas** para almacenar datos de manera persistente.

---

### ✅ Arquitectura

- **FastAPI** expone dos endpoints para crear envíos y registrar eventos.
- **Redis** o **GCP Pub/Sub** actúan como bus de mensajes (dependiendo de configuración).
- **Consumers** escuchan eventos y realizan persistencia real (MongoDB) y análisis.
- **MongoDB Atlas** almacena de forma persistente los mensajes/eventos procesados.

---

### 🗺️ Flujo de eventos

1️⃣ POST `/v1/shipments`: Publica un evento al canal `shipments`.

2️⃣ `integration_consumer`: Escucha `shipments`, procesa la creación del envío y lo guarda en MongoDB.

3️⃣ POST `/v1/shipment-events`: Publica al canal `shipment_events`.

4️⃣ `event_consumer`: Escucha `shipment_events`, deduplica y guarda eventos únicos en MongoDB.

5️⃣ `data_analysis_consumer`: Escucha `shipment_events`, procesa eventos `COMPLETED` y `REJECTED`, y actualiza métricas.

---

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
│   ├── redis_client.py
│   └── mongo_client.py
├── models/
│   ├── shipment.py
│   └── shipment_event.py
├── services/
│   └── message_bus.py
└── main.py
```

---

### 🚀 Instalación

```bash
python -m venv venv
venv\Scripts\activate       # En Windows
pip install -r requirements.txt
```

---

### ▶️ Ejecutar API

```bash
uvicorn app.main:app --reload
```

---

### ▶️ Ejecutar Consumers

```bash
python -m app.consumers.integration_consumer
python -m app.consumers.event_consumer
python -m app.consumers.data_analysis_consumer
```

---

### 🧪 Probar

- Accede a `http://localhost:8000/docs` para probar los endpoints interactivos.
- Observa logs en consola para confirmar la ejecución de los consumers.

---

### 🧪 Pruebas Unitarias

Para ejecutar pruebas con **pytest**:

```bash
pytest
```

> Asegúrate de tener `pytest` instalado:
```bash
pip install pytest
```

---

## 💾 Conexión a MongoDB Atlas

- Configura tu archivo `.env` con:

```dotenv
MONGO_URI=mongodb+srv://<usuario>:<contraseña>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
MONGO_DB=shipment_system
```

- Las colecciones generadas automáticamente son:
  - `shipment_system.shipments`
  - `shipment_system.shipment_events`

---

## ⚙️ Variables de Entorno

Ejemplo de `.env`:

```dotenv
BUS_BACKEND=pubsub  # O redis
GCP_PROJECT_ID=traxion-shipment-system
GOOGLE_APPLICATION_CREDENTIALS=C:/ruta/credenciales.json
MONGO_URI=mongodb+srv://admin:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
MONGO_DB=shipment_system
```

---

## 📦 Requerimientos

```
fastapi
uvicorn
redis
pydantic
python-dotenv
google-cloud-pubsub
pymongo
pytest
```

---

## 📌 Diagrama del Servicio

```
                +--------------------------+
                |       Cliente API        |
                +------------+-------------+
                             |
                             v
                  +-------------------+
                  |     FastAPI       |
                  |  (Producers)      |
                  +-----+-----+-------+
                        |     |
                        |     |
            +-----------+     +-------------+
            |                           |
            v                           v
   Publish to Pub/Sub           Publish to Pub/Sub
     topic "shipments"           topic "shipment_events"
            |                           |
            |                           |
   +--------v---------+         +-------v----------+
   | Integration      |         | Event Consumer  |
   | Consumer         |         | (deduplica + DB)|
   +--------+---------+         +-------+----------+
            |                           |
            v                           v
    MongoDB: shipments         MongoDB: shipment_events
                                     |
                                     v
                            +-------------------------+
                            | Data Analysis Consumer  |
                            | (COMPLETED/REJECTED)   |
                            +-----------+-------------+
                                        |
                                        v
                           Guarda conteos y métricas
```

---

### 🔐 Seguridad

Asegúrate de que el archivo `.env` **NO** se suba a GitHub. Agrega esta línea al `.gitignore`:
```bash
.env
```

---

### ✨ Autor
- Proyecto elaborado para prácticas de arquitectura orientada a eventos con Pub/Sub, Redis y MongoDB.
