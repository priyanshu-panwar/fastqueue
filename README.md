# FastQueue

🦄FastQueue is a lightweight, self-hosted message queue system inspired by AWS SQS. It's designed for small-scale, cost-conscious developers who want reliability, observability, and speed—without relying on managed services.

---

## Docs

<p>Refer here for detailed <a href="https://priyanshu-panwar.github.io/fastqueue/" target="_blank">docs</a>.</p>

---

## 🚀 Features

- **Queue Management**: Queue creation, deletion, and listing
- **Message Operations**: Message publishing (produce) and consuming (receive/delete)
- **Authentication**: Lightweight token-based auth (JWT)
- **User Management**: User management via API and CLI
- **Observability**: Built-in observability and performance metrics
- **Performance**: Redis-based caching for speed
- **CLI Support**: CLI support for queue and auth operations
- **Production Ready**: Pythonic and production-ready Docker setup
- **Coming Soon**: Dead Letter Queue (DLQ) support and persistent message storage

---

## ⚡ Quick Start

### Using Docker (Recommended)

```bash
# Pull and run the latest image
docker pull priyanshu009ch/fastqueue:latest
docker run -d -p 9080:9080 --name fastqueue priyanshu009ch/fastqueue:latest
```

### Using Source Code

```bash
# Clone the repository
git clone https://github.com/your-org/fastqueue.git
cd fastqueue

# Quick start with make
make run
```

**Manual setup:**

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 9080
```

### Access the CLI

```bash
# Enter the Docker container
docker exec -it fastqueue bash

# Use the CLI
python -m cli.main --help
```

---

## 📖 Documentation

<div class="docs-grid">
  <div class="doc-card">
    <h3><a href="./api">🔌 API Reference</a></h3>
    <p>Complete REST API documentation for authentication, queue management, and message operations.</p>
  </div>
  
  <div class="doc-card">
    <h3><a href="./cli">⚡ CLI Commands</a></h3>
    <p>Command-line interface documentation for managing users and queues from the terminal.</p>
  </div>
</div>

---

## 🏗️ Architecture

FastQueue is built with modern Python technologies:

- **FastAPI**: High-performance async web framework
- **SQLAlchemy**: Database ORM for persistent storage
- **Redis**: High-speed caching and message queuing
- **JWT**: Secure token-based authentication
- **Docker**: Containerized deployment
- **Typer**: Beautiful CLI interface

---

## 🔧 Configuration

FastQueue can be configured through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `JWT_SECRET_KEY` | Secret key for access tokens | Auto-generated |
| `JWT_REFRESH_SECRET_KEY` | Secret key for refresh tokens | Auto-generated |
| `max_queue_length`  | max no of messages in queue at a time | 10000 (can be changed)|

---

## 🚀 Examples

### Creating Your First Queue

```bash
# Using CLI
python -m cli.main queue create

# Using API
curl -X POST "http://localhost:9080/queues" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-queue", "max_length": 1000}'
```

### Sending a Message

```bash
curl -X POST "http://localhost:9080/queue/my-queue" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "Action": "SendMessage",
    "MessageBody": "Hello, FastQueue!"
  }'
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/priyanshu009ch/fastqueue/blob/main/CONTRIBUTING.md) for details.

---

## 📄 License

FastQueue is released under the [MIT License](https://github.com/priyanshu009ch/fastqueue/blob/main/LICENSE).

---

## 🔗 Links

- [GitHub Repository](https://github.com/priyanshu009ch/fastqueue)
- [Docker Hub](https://hub.docker.com/r/priyanshu009ch/fastqueue)
- [Docs](https://priyanshu-panwar.github.io/fastqueue/)
