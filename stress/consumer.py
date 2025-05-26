import httpx
import asyncio
import os

API_KEY = os.getenv("API_KEY", "default_api_key")
QUEUE_NAME = os.getenv("QUEUE_NAME", "test-queue")
BASE_URL = os.getenv("BASE_URL", "http://localhost:9080")

HEADERS = {"Authorization": f"Bearer {API_KEY}"}


async def poll_and_delete(session):
    try:
        response = await session.post(
            f"{BASE_URL}/v1/queue/{QUEUE_NAME}",
            json={"Action": "ReceiveMessage", "MaxNumberOfMessages": 10},
            headers=HEADERS,
        )
        messages = response.json().get("Messages", [])
        for msg in messages:
            rh = msg["ReceiptHandle"]
            await session.post(
                f"{BASE_URL}/v1/queue/{QUEUE_NAME}",
                json={"Action": "DeleteMessage", "ReceiptHandle": rh},
                headers=HEADERS,
            )
        return len(messages)
    except Exception as e:
        print(f"Error: {e}")
        return 0


async def consumer():
    async with httpx.AsyncClient() as session:
        while True:
            count = await poll_and_delete(session)
            print(f"Received and deleted {count} messages")
            if count == 0:
                await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(consumer())
