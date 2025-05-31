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

## 🚀 Getting Started

This section will walk you through the complete process of setting up FastQueue, getting an access token, creating a queue, sending messages, and receiving messages.

### Step 1: Start FastQueue Server

```bash
# Using Docker (Recommended)
docker pull priyanshu009ch/fastqueue:latest
docker run -d -p 9080:9080 --name fastqueue priyanshu009ch/fastqueue:latest

# Or using source code
git clone https://github.com/priyanshu-panwar/fastqueue.git
cd fastqueue
make run
```

### Step 2: Get Access Token

You can either use the default admin user or register a new user.

#### Option A: Use Default Admin User (Recommended for Quick Start)

Login with the default admin credentials:

```bash
curl -X POST "http://localhost:9080/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

#### Option B: Register a New User

First, register a new user:

```bash
curl -X POST "http://localhost:9080/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

**Response:**
```json
{
  "username": "testuser"
}
```

Then login to get your access token:

```bash
curl -X POST "http://localhost:9080/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Save your access token** - you'll need it for all subsequent operations!

### Step 3: Create Your First Queue

```bash
curl -X POST "http://localhost:9080/v1/queues" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-first-queue", "max_length": 1000, "visibility_timeout": 30}'
```

**Response:**
```json
{
  "name": "my-first-queue",
  "message_count": 0,
  "max_length": 1000,
  "visibility_timeout": 30
}
```

### Step 4: Verify Queue Creation

List all queues to confirm your queue was created:

```bash
curl -X GET "http://localhost:9080/v1/queues" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**Response:**
```json
{
  "queues": [
    {
      "name": "my-first-queue",
      "message_count": 0,
      "max_length": 1000,
      "visibility_timeout": 30
    }
  ]
}
```

### Step 5: Send Your First Message

```bash
curl -X POST "http://localhost:9080/v1/queue/my-first-queue" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "Action": "SendMessage",
    "MessageBody": "Hello, FastQueue! This is my first message.",
    "MessageAttributes": {
      "priority": "high",
      "type": "test"
    }
  }'
```

**Response:**
```json
{
  "MessageId": "abc123",
  "status": "sent"
}
```

### Step 6: Receive Messages

```bash
curl -X POST "http://localhost:9080/v1/queue/my-first-queue" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "Action": "ReceiveMessage",
    "MaxNumberOfMessages": 1
  }'
```

**Response:**
```json
{
  "Messages": [
    {
      "MessageId": "abc123",
      "Body": "Hello, FastQueue! This is my first message.",
      "Attributes": {
        "priority": "high",
        "type": "test"
      },
      "ReceiptHandle": "receipt_handle_123"
    }
  ]
}
```

### Step 7: Delete the Message (Optional)

After processing the message, delete it from the queue:

```bash
curl -X POST "http://localhost:9080/v1/queue/my-first-queue" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "Action": "DeleteMessage",
    "ReceiptHandle": "receipt_handle_123"
  }'
```

**Response:**
```json
{
  "message": "Message deleted successfully"
}
```

### 🎉 You're All Set!

You've successfully:
- ✅ Started FastQueue server
- ✅ Registered a user and obtained an access token
- ✅ Created your first queue
- ✅ Sent a message to the queue
- ✅ Received and processed the message
- ✅ Deleted the message from the queue


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
