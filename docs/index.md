---
layout: default
title: FastQueue Documentation
description: 🦄 A lightweight, self-hosted message queue system inspired by AWS SQS
---

# FastQueue

🦄 FastQueue is a lightweight, self-hosted message queue system inspired by AWS SQS. It's designed for small-scale, cost-conscious developers who want reliability, observability, and speed—without relying on managed services.

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

## 🚀 Getting Started

This section will walk you through the complete process of setting up FastQueue, getting an access token, creating a queue, sending messages, and receiving messages.

### Step 1: Start FastQueue Server

#### Option A: Using Docker with Environment Variables (Recommended)

```bash
# Pull the latest image
docker pull priyanshu009ch/fastqueue:latest

# Run with custom environment variables
docker run -d -p 9080:9080 --name fastqueue \
  -e JWT_SECRET_KEY="your_super_secret_jwt_key_here" \
  -e JWT_REFRESH_SECRET_KEY="your_super_secret_refresh_key_here" \
  -e max_queue_length=5000 \
  -e debug=true \
  priyanshu009ch/fastqueue:latest
```

#### Option B: Using Docker with .env File

Create a `.env` file with your configuration:

```bash
# Create .env file
cat > .env << EOF
# Authentication
JWT_SECRET_KEY=your_super_secret_jwt_key_here
JWT_REFRESH_SECRET_KEY=your_super_secret_refresh_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_MINUTES=10080

# Queue Settings
max_queue_length=5000
visibility_timeout_seconds=30
restore_interval_ms=500

# Default Admin User
default_username=admin
default_password=password

# Cache Settings
verify_token_cache_ttl_seconds=900
verify_token_cache_maxsize=100
EOF

# Run Docker with .env file
docker run -d -p 9080:9080 --name fastqueue \
  --env-file .env \
  priyanshu009ch/fastqueue:latest
```

#### Option C: Using Source Code

```bash
# Clone the repository
git clone https://github.com/priyanshu-panwar/fastqueue.git
cd fastqueue

# Create your .env file (optional)
cp .env.example .env  # if available, or create manually

# Quick start with make
make run

# Or manual setup
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 9080
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

### Quick Troubleshooting

If you encounter "queue not exist" errors:

1. **Check your access token**: Make sure you're using the correct token from the login response
2. **Verify queue name**: Ensure the queue name in your message operations matches exactly
3. **Check URL format**: Use `/v1/queue/{name}` for message operations, not `/v1/queues/{name}`
4. **List queues**: Always verify the queue exists with `GET /v1/queues` before sending messages
5. **Check server logs**: Look at FastQueue server logs for detailed error messages

### Next Steps

- Explore the [CLI Commands](./cli) for terminal-based operations
- Check out the complete [API Reference](./api) for advanced features
- Set up monitoring and observability for production use

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

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/priyanshu009ch/fastqueue/blob/main/CONTRIBUTING.md) for details.

---

## 📄 License

FastQueue is released under the [MIT License](https://github.com/priyanshu009ch/fastqueue/blob/main/LICENSE).

---

## 🔗 Links

- [GitHub Repository](https://github.com/priyanshu009ch/fastqueue)
- [Docker Hub](https://hub.docker.com/r/priyanshu009ch/fastqueue)
- [Issues & Bug Reports](https://github.com/priyanshu009ch/fastqueue/issues)

<style>
.docs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.doc-card {
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  padding: 1.5rem;
  background: #f8f9fa;
}

.doc-card h3 {
  margin-top: 0;
  color: #0366d6;
}

.doc-card h3 a {
  text-decoration: none;
  color: inherit;
}

.doc-card h3 a:hover {
  text-decoration: underline;
}

.doc-card p {
  color: #586069;
  margin-bottom: 0;
}
</style>