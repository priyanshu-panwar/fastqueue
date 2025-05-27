import httpx
import asyncio
import os
import time

API_KEY = os.getenv("API_KEY", "default_api_key")
QUEUE_NAME = os.getenv("QUEUE_NAME", "test-queue")
BASE_URL = os.getenv("BASE_URL", "http://localhost:9080")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

cnt = 0
consumer_latencies = []
MAX_NUMBER_OF_MESSAGES = 1


async def poll_and_delete(session):
    try:
        start = time.perf_counter()
        response = await session.post(
            f"{BASE_URL}/v1/queue/{QUEUE_NAME}",
            json={
                "Action": "ReceiveMessage",
                "MaxNumberOfMessages": MAX_NUMBER_OF_MESSAGES,
            },
            headers=HEADERS,
        )
        latency = (time.perf_counter() - start) * 1000  # Convert to ms
        consumer_latencies.append(latency)

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


async def consumer(expected_messages: int):
    global cnt
    start = time.perf_counter()
    attempts = 0

    async with httpx.AsyncClient() as session:
        while (
            cnt < expected_messages * 2
        ):  # Allow some buffer for processing also validate we don't receive messages that were deleted
            count = await poll_and_delete(session)
            cnt += count
            if cnt % 1000 == 0:
                print(f"Processed {cnt} messages")

            if count == 0:
                attempts += 1
                await asyncio.sleep(0.5)
                if attempts > 5:
                    print(f"Still no messages after {attempts} attempts")
                    break

    duration = time.perf_counter() - start
    print(f"\n🎯 Consumer Summary:")
    print(f"Total messages processed: {cnt}")
    print(f"Total time: {duration:.2f} seconds")
    print(f"Avg latency: {sum(consumer_latencies) / len(consumer_latencies):.2f} ms")
    print(f"Throughput: {cnt / duration:.2f} messages/sec")


# if __name__ == "__main__":
#     import asyncio

#     TOTAL_MESSAGES = 10000
#     asyncio.run(consumer(expected_messages=TOTAL_MESSAGES))
