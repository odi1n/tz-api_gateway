import asyncio
import json
from enum import Enum
from typing import Optional

import aio_pika
from pydantic import BaseModel

from settings import setting

LOOP = asyncio.get_event_loop()


class QueueType(str, Enum):
    PLUS = "plus"
    RESULT_PLUS = "result_plus"


class QueueRequest(BaseModel):
    queue: QueueType
    values: list[int]


class QueueResult(BaseModel):
    queue: QueueType
    val_sum: int


async def send(queue_model: QueueRequest) -> None:
    connection = await aio_pika.connect_robust(url=setting.amqp_url)

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(name=queue_model.queue.value)

        await channel.default_exchange.publish(
            message=aio_pika.Message(body=queue_model.json().encode()),
            routing_key=queue.name,
        )


async def receiving(queue_type: QueueType) -> Optional[QueueResult]:
    connection = await aio_pika.connect_robust(url=setting.amqp_url)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(name=queue_type.value)
        data_parse = None

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = message.body.decode()

                    if queue.name in data:
                        data_parse = json.loads(data)
                        break

        if data_parse:
            return QueueResult(**data_parse)

        return None
