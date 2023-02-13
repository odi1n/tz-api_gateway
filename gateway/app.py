from typing import Optional

from fastapi import FastAPI

from queues import QueueRequest, QueueResult, QueueType, receiving, send

app = FastAPI(
    title="Microservice Telegram",
    version="0.1.0",
)


@app.post(path="/api/sum")
async def sum_values(values: list[int]) -> Optional[QueueResult]:
    """
    ## Sum values

    * **values** (_not implemented_). - Integer list values
    """
    await send(queue_model=QueueRequest(queue=QueueType.PLUS, values=values))
    return await receiving(queue_type=QueueType.RESULT_PLUS)
