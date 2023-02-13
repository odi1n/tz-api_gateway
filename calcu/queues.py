import json
from enum import Enum
from typing import Optional

import aio_pika
from pydantic import BaseModel

from settings import setting


class QueueType(str, Enum):
    PLUS = "plus"
    RESULT_PLUS = "result_plus"


class QueueRequest(BaseModel):
    queue: QueueType
    values: list[int]


class QueueResult(BaseModel):
    queue: QueueType
    val_sum: int


async def send(queue_model: QueueResult) -> None:
    connection = await aio_pika.connect_robust(url=setting.amqp_url)

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(name=queue_model.queue.value)

        await channel.default_exchange.publish(
            message=aio_pika.Message(body=queue_model.json().encode()),
            routing_key=queue.name,
        )


async def receiving(queue_type: QueueType) -> Optional[QueueRequest]:
    connection = await aio_pika.connect_robust(url=setting.amqp_url)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(name=queue_type.value)
        js = None

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = message.body.decode()

                    if queue.name in data:
                        js = json.loads(data)
                        break
        if js:
            return QueueRequest(**js)
        return None
