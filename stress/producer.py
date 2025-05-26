import httpx
import asyncio
import os

API_KEY = os.getenv("API_KEY", "default_api_key")
QUEUE_NAME = os.getenv("QUEUE_NAME", "test-queue")
BASE_URL = os.getenv("BASE_URL", "http://localhost:9080")

HEADERS = {"Authorization": f"Bearer {API_KEY}"}


async def send_message(session, message_num):
    payload = {
        "Action": "SendMessage",
        "MessageBody": f"Hello FastQueue! Message {message_num}",
    }
    try:
        response = await session.post(
            f"{BASE_URL}/v1/queue/{QUEUE_NAME}", json=payload, headers=HEADERS
        )
        if response.status_code != 200:
            print(f"Failed to send {message_num}: {response.text}")
        print(f"Sent message {message_num}: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")


async def producer(n_messages: int = 1000, concurrency: int = 100):
    async with httpx.AsyncClient() as session:
        sem = asyncio.Semaphore(concurrency)

        async def bound_send(i):
            async with sem:
                await send_message(session, i)

        await asyncio.gather(*(bound_send(i) for i in range(n_messages)))


if __name__ == "__main__":
    asyncio.run(producer())
