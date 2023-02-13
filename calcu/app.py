import asyncio

from queues import QueueResult, QueueType, receiving, send


async def main() -> None:
    while True:
        queue_model = await receiving(queue_type=QueueType.PLUS)
        if queue_model is None:
            continue

        await send(
            queue_model=QueueResult(
                queue=QueueType.RESULT_PLUS, val_sum=sum(queue_model.values)
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
