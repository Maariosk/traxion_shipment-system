# Sistema de Gestión de Envíos 📦 - ¡Guía Rápida para Levantar el Servicio!

Este es el repositorio del **Sistema de Gestión de Envíos**. La idea central aquí es simular cómo manejamos los paquetes y todos los eventos que ocurren en su ciclo de vida (desde que se registra hasta que se entrega o se rechaza). Todo esto lo hacemos con una **arquitectura basada en eventos**, lo que significa que tenemos varios servicios pequeños y **desacoplados** que se comunican entre sí usando un "bus de mensajes". Esto nos ayuda a mantener las cosas ordenadas y flexibles.

---

## 🚀 Cómo replicar esto

Aquí te explico cómo dejar todo listo y funcionando en tu máquina para que puedas probarlo y empezar a trabajar.

### Lo que Vas a Necesitar (Prerrequisitos)

* **Python 3.11.0** (o una versión más reciente, ¡siempre es bueno estar actualizado!).
* **pip** (el gestor de paquetes de Python, que normalmente viene con Python).
* **Memurai** (una alternativa a Redis para Windows, ¡muy útil!). Descárgalo e instálalo desde [https://www.memurai.com/](https://www.memurai.com/). Asegúrate de que esté corriendo en el puerto por defecto (6379).

### Pasos de Instalación (¡Fácil y Rápido!)

1.  **Clona este repositorio:**
    Abre tu terminal o línea de comandos y ejecuta:
    ```bash
    git clone https://[https://github.com/tu-usuario/nombre-de-tu-repositorio.git](https://github.com/tu-usuario/nombre-de-tu-repositorio.git)
    cd nombre-de-tu-repositorio
    ```
    *No olvides reemplazar `tu-usuario` por tu nombre de usuario de GitHub y `nombre-de-tu-repositorio` por el nombre real del repositorio donde lo tienes.*

2.  **Crea y activa un entorno virtual (¡Altamente recomendado!):**
    Esto es una buena práctica para que las dependencias de este proyecto no se mezclen con las de otros.
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instala las dependencias necesarias:**
    Asegúrate de que tengas un archivo `requirements.txt` en la raíz de tu proyecto con todas las bibliotecas que tu código necesita. Un ejemplo básico podría ser:
    ```
    # requirements.txt
    Flask
    redis  # Para conectarse a Memurai/Redis
    # Agrega cualquier otra dependencia que uses
    ```
    Luego, instala todo con este comando:
    ```bash
    pip install -r requirements.txt
    ```

---

## ⚙️ Cómo Levantar los Servicios

Este sistema está compuesto por varios servicios que se ejecutan de forma independiente y se comunican a través del bus de mensajes. Deberás iniciar cada uno en su propia terminal.

### 1. El Bus de Mensajes 🚌 (¡El Centro de Comunicación!)

Aquí es donde todos los eventos se publican y se consumen. Para este proyecto, usaremos **Memurai** (que es compatible con la API de Redis).

* **Asegúrate de que Memurai esté funcionando:**
    Si lo instalaste, debería estar corriendo en segundo plano. Puedes verificarlo yendo al *Task Manager* en Windows o usando herramientas de Memurai. Por defecto, escuchará en el puerto `6379`.

### 2. Los Publicadores 📤 (¡Los que Emiten Eventos!)

Estos servicios son los que exponen los *endpoints* a los que le pegamos para crear nuevos envíos o registrar eventos sobre envíos ya existentes.

* **Servicio de Registro de Envíos (`POST v1/shipments`):**
    Este *endpoint* se encarga de iniciar el proceso de una nueva orden. Lo único que hace es **enviar un evento al bus de mensajes** con la información para registrar un nuevo envío.
    * **Ejemplo de *Payload*:**
        ```json
        {
          "id": "UNICO_SHIPMENT_ID_XYZ",          // Identificador único para el envío
          "origin_date": "2025-07-14T10:00:00Z",  // Fecha y hora de la solicitud de creación
          "item_amount": 999.00                   // Monto del artículo asociado al envío
        }
        ```
        

* **Servicio de Eventos de Envío (`POST v1/shipment-events`):**
    Este *endpoint* nos permite registrar cualquier evento que ocurra con un envío existente (como `INTEGRATED`, `ON_ROUTE`, `TRANSPORT_ARRIVAL`, `COMPLETED`, `REJECTED`). Este servicio **publica** estos eventos al bus de mensajes.
    * **Ejemplo de *Payload*:**
        ```json
        {
          "shipment_id": "UNICO_SHIPMENT_ID_XYZ",    // El ID del envío al que se refiere el evento
          "event": "INTEGRATED",                     // Tipo de evento (INTEGRATED, ON_ROUTE, etc.)
          "origin_date": "2025-07-14T10:05:00Z",     // Fecha y hora física en que ocurrió el evento
          "author": "SistemaLogistica"               // Identificador de quién o qué generó el evento
        }
        ```
        

* **Para iniciar los servicios publicadores (por ejemplo, si usas Flask):**
    Abre una nueva terminal y ejecuta:
    ```bash
    python src/publishers/api.py
    ```
    *(Asegúrate de ajustar la ruta si tu archivo principal de publicadores está en otro lugar, por ejemplo: `python src/interfaces/api.py`)*

### 3. Los Consumidores 📥 (¡Los que Escuchan y Procesan!)

Estos servicios están suscritos al bus de mensajes y actúan sobre los eventos que reciben. Deberás iniciar cada uno en una terminal diferente para que funcionen correctamente.

* **`integration-consumer`:**
    Este consumidor está atento a los eventos de **creación de envíos** y se encarga de guardar los detalles del nuevo envío en nuestra base de datos (o repositorio de datos).
    ```bash
    python src/consumers/integration_consumer.py
    ```

* **`event-consumer`:**
    Este escucha **todos los eventos** que pasan por el bus y los persiste en el repositorio de datos. Un detalle importante es que también se encarga de la **deduplicación de eventos**, para evitar guardar la misma información varias veces. [cite: 53]
    ```bash
    python src/consumers/event_consumer.py
    ```

* **`data-analysis-consumer`:**
    Este es un poco más específico. Solo le interesan los eventos de `COMPLETED` (completado) y `REJECTED` (rechazado). Su trabajo es llevar un conteo de los `SHIPMENTS_TOTALES` (total de envíos procesados) y `SHIPMENTS_ENTREGADOS` (envíos completados con éxito) en un repositorio de datos separado, que usamos para un análisis "simulado" de la información. [cite: 54]
    * **Ejemplo de *Payload* (lo que recibiría este consumidor):**
        ```json
        {
          "shipment_id": "UNICO_SHIPMENT_ID_XYZ",     // El ID del envío
          "event": "COMPLETED",                      // El tipo de evento (COMPLETED o REJECTED)
          "origin_date": "2025-07-14T11:30:00Z",      // Fecha y hora física en que ocurrió el evento
          "author": "SistemaDeLogistica"              // Quién o qué generó el evento
        }
        ```
        
    ```bash
    python src/consumers/data_analysis_consumer.py
    ```
    *(¡Recuerda ajustar las rutas de los consumidores si tu estructura de carpetas es diferente!)*

---

## 🏗️ Cómo Está Organizado el Código

El proyecto sigue algunos principios clave de **arquitectura basada en eventos**, con **servicios bien desacoplados** y una **estructura de carpetas clara** para que cada parte tenga su responsabilidad definida.
```bash
shipment-system/
│
├── app/
│   ├── api/             # Endpoints HTTP (FastAPI)
│   │   ├── shipments.py
│   │   ├── shipment_events.py
│   │   └── __init__.py
│   │
│   ├── consumers/       # Consumers (integration, event, data analysis)
│   │   ├── integration_consumer.py
│   │   ├── event_consumer.py
│   │   ├── data_analysis_consumer.py
│   │   └── __init__.py
│   │
│   ├── core/            # Configuración (Redis, settings)
│   │   ├── config.py
│   │   ├── redis_client.py
│   │   └── __init__.py
│   │
│   ├── models/          # Modelos y entidades
│   │   ├── shipment.py
│   │   ├── shipment_event.py
│   │   └── __init__.py
│   │
│   ├── services/        # Lógica de negocio
│   │   ├── message_bus.py
│   │   └── __init__.py
│   │
│   └── main.py          # Entry point FastAPI
│
├── requirements.txt
├── README.md
└── pyproject.toml (opcional)

```

---

## 🧪 Pruebas (¡Para Asegurarnos que Todo Funciona!)

Siempre es bueno tener **pruebas unitarias** para cada componente, así nos aseguramos de que cada pieza hace lo que se espera.

Para correr las pruebas (si ya las tienes implementadas):
```bash
pytest
(Si no tienes pytest instalado, puedes agregarlo con pip install pytest)