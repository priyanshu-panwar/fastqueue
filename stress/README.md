# FastQueue Stress Test

This folder contains a **producer-consumer stress testing framework** designed to evaluate the performance and reliability of the Fastqueue message queue system under high load conditions.

## 📌 Purpose

The goal of this test is to:

- Simulate **high-throughput message production and consumption**.
- Measure **latency, throughput, and concurrency handling**.
- Validate FastQueue’s ability to **handle thousands of messages** with multiple concurrent producers and consumers.
- Guaranteed delivery of messages

## 📁 Structure

```
stress/
├── producer.py   # Async producer that sends messages to a FastQueue queue
├── consumer.py   # Async consumer that polls and deletes messages from the queue
└── main.py       # Entry point that runs producer and consumer concurrently
```

---

## 🚀 How It Works

- The **producer** rapidly sends messages to a configured queue using multiple concurrent workers (controlled by `asyncio.Semaphore`).
- The **consumer** continuously pulls and deletes messages from the queue.
- Both use the FastQueue HTTP API via `httpx.AsyncClient`.

---

## ⚙️ Configuration

- Target URL: `http://localhost:9080`
- Default queue name: `stress-test`
- Default number of messages: `10,000`
- Default concurrency: `200 producers`
- Authorization: Uses API key from `settings.api_key`

To modify the behavior, edit values in `producer.py`, `consumer.py`, or pass parameters into `producer()` or `consumer()`.

---

## 🧪 How to Run

> Ensure FastQueue is running locally at `http://localhost:9080`.

### 1. Install dependencies

```bash
poetry install
```

### 2. Run the stress test

```bash
cd stress
python main.py
```
This will run both producer and consumer asynchronously until all messages are sent and received.

OR you can individually run producer consumer
```bash
cd stress
python producer.py
python consumer.py
```

---
