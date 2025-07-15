from app.core.redis_client import r
from typing import Any

class MessageBus:
    def publish(self, channel: str, message: str) -> None:
        r.publish(channel, message)

bus = MessageBus()
