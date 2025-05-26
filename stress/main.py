import asyncio
from producer import producer
from consumer import consumer


async def main():
    await asyncio.gather(producer(n_messages=10, concurrency=2), consumer())


if __name__ == "__main__":
    asyncio.run(main())
