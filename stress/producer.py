import httpx
import asyncio
import os
import time

API_KEY = os.getenv("API_KEY", "default_api_key")
QUEUE_NAME = os.getenv("QUEUE_NAME", "test-queue")
BASE_URL = os.getenv("BASE_URL", "http://localhost:9080")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

cnt = 0
producer_latencies = []


async def send_message(session, message_num):
    payload = {
        "Action": "SendMessage",
        "MessageBody": f"Hello FastQueue! Message {message_num}",
    }
    try:
        start = time.perf_counter()
        response = await session.post(
            f"{BASE_URL}/v1/queue/{QUEUE_NAME}", json=payload, headers=HEADERS
        )
        latency = (time.perf_counter() - start) * 1000  # Convert to ms
        producer_latencies.append(latency)

        if response.status_code != 200:
            print(f"Failed to send {message_num}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")


async def producer(n_messages: int = 1000, concurrency: int = 100):
    global cnt
    start = time.perf_counter()

    async with httpx.AsyncClient() as session:
        sem = asyncio.Semaphore(concurrency)

        async def bound_send(i):
            async with sem:
                global cnt
                cnt += 1
                if cnt % 1000 == 0:
                    print(f"Sent {cnt} messages")
                await send_message(session, i)

        await asyncio.gather(*(bound_send(i) for i in range(n_messages)))

    duration = time.perf_counter() - start
    print(f"\n🎯 Producer Summary:")
    print(f"Total messages sent: {cnt}")
    print(f"Total time: {duration:.2f} seconds")
    print(f"Avg latency: {sum(producer_latencies) / len(producer_latencies):.2f} ms")
    print(f"Throughput: {cnt / duration:.2f} messages/sec")


# if __name__ == "__main__":
#     asyncio.run(producer(n_messages=10000, concurrency=100))
