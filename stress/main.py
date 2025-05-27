import asyncio
from producer import producer
from consumer import consumer

TOTAL_MESSAGES = 10000
CONCURRENCY = 100


async def main():
    await asyncio.gather(
        producer(n_messages=TOTAL_MESSAGES, concurrency=CONCURRENCY),
        consumer(expected_messages=TOTAL_MESSAGES),
    )


if __name__ == "__main__":
    asyncio.run(main())
