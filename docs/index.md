# FastQueue

FastQueue is a lightweight, self-hosted message queue system inspired by AWS SQS. It's designed for small-scale, cost-conscious developers who want reliability, observability, and speed—without relying on managed services.

---

## 🚀 Features

- Queue creation, deletion, and listing
- Message publishing (produce) and consuming (receive/delete)
- Lightweight token-based auth (JWT)
- User management via API and CLI
- Built-in observability and performance metrics
- Redis-based caching for speed
- CLI support for queue and auth operations
- Pythonic and production-ready Docker setup
- Dead Letter Queue (DLQ) support (to be added)
- Persistent message storage (to be added)

---

## 📦 Installation & Usage

### Using Docker (Recommended)

```bash
docker pull priyanshu009ch/fastqueue:latest
docker run -d -p 9080:9080 --name fastqueue priyanshu009ch/fastqueue:latest
```

### Using Source Code

```bash
git clone https://github.com/your-org/fastqueue.git
cd fastqueue
make run
```

> Or you can run manually:

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 9080
```

### Access the CLI inside Docker

```bash
docker exec -it fastqueue bash
python -m cli.main --help
```

---

## 📚 Documentation Pages

- [CLI Commands](./cli.md)
- [API Reference](./api.md)

---