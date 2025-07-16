import os
import json
from enum import Enum
from typing import Literal
from dotenv import load_dotenv

# Cargar variables desde .env si existe
load_dotenv()

# Selección dinámica de bus
class BusType(str, Enum):
    REDIS = "redis"
    PUBSUB = "pubsub"

BUS_BACKEND: Literal["redis", "pubsub"] = os.getenv("BUS_BACKEND", "redis").lower()

# Redis setup
try:
    import redis
    r = redis.Redis(host='localhost', port=6379, db=0)
except ImportError:
    r = None

# GCP Pub/Sub setup
try:
    from google.cloud import pubsub_v1
    from google.api_core.exceptions import NotFound

    # Cargar ruta de credenciales desde la variable de entorno
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path or not os.path.exists(credentials_path):
        raise RuntimeError(f"Credenciales GCP no encontradas en: {credentials_path}")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    project_id = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
except ImportError:
    publisher = None
    subscriber = None


def publish(topic: str, message: str) -> None:
    if BUS_BACKEND == BusType.REDIS:
        if not r:
            raise RuntimeError("Redis client not available. Make sure redis-py is installed.")
        r.publish(topic, message)
        print(f"[REDIS] Published to {topic}: {message}")

    elif BUS_BACKEND == BusType.PUBSUB:
        if not publisher:
            raise RuntimeError("GCP Pub/Sub client not available. Make sure google-cloud-pubsub is installed.")
        topic_path = publisher.topic_path(project_id, topic)
        try:
            publisher.get_topic(topic=topic_path)  # Ensure topic exists
        except NotFound:
            publisher.create_topic(name=topic_path)
        future = publisher.publish(topic_path, message.encode("utf-8"))
        print(f"[PUBSUB] Published to {topic}: {message} [msg ID: {future.result()}]")

    else:
        raise ValueError(f"Unsupported BUS_BACKEND: {BUS_BACKEND}")


def subscribe(topic: str, callback):
    if BUS_BACKEND == BusType.REDIS:
        if not r:
            raise RuntimeError("Redis client not available.")
        pubsub = r.pubsub()
        pubsub.subscribe(topic)
        print(f"[REDIS] Subscribed to {topic}")
        for message in pubsub.listen():
            if message['type'] == 'message':
                callback(message['data'].decode())

    elif BUS_BACKEND == BusType.PUBSUB:
        if not subscriber:
            raise RuntimeError("GCP Pub/Sub subscriber not available.")
        topic_path = publisher.topic_path(project_id, topic)
        subscription_path = subscriber.subscription_path(project_id, f"sub-{topic}")
        try:
            subscriber.get_subscription(subscription=subscription_path)
        except NotFound:
            subscriber.create_subscription(name=subscription_path, topic=topic_path)

        def gcp_callback(message):
            callback(message.data.decode())
            message.ack()

        future = subscriber.subscribe(subscription_path, callback=gcp_callback)
        print(f"[PUBSUB] Subscribed to {topic}")
        return future

    else:
        raise ValueError(f"Unsupported BUS_BACKEND: {BUS_BACKEND}")


# Instancia de bus para importar fácilmente desde otros módulos
class MessageBus:
    def __init__(self):
        self.publish = publish
        self.subscribe = subscribe

bus = MessageBus()
