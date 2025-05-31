# API Reference

This document outlines the REST APIs provided by FastQueue for authentication, queue management, and message operations.

---

## Base URL

```
http://localhost:9080/v1
```

---

## Authentication APIs

All queue and message operations require authentication. You can use either JWT tokens or API keys.

### Register User

**POST** `/auth/register`

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "username": "your_username"
}
```

---

### Login

**POST** `/auth/login`

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### Refresh Token

**POST** `/auth/refresh`

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### Change Password

**POST** `/auth/change-password`

**Request Body:**
```json
{
  "username": "your_username",
  "old_password": "old_password",
  "new_password": "new_password"
}
```

**Response:**
```json
{
  "username": "your_username"
}
```

---

### Delete User

**POST** `/auth/delete`

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "message": "User deleted successfully"
}
```

---

## Queue APIs

**Note:** All queue operations require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

### Create a Queue

**POST** `/queues`

**Request Body:**
```json
{
  "name": "queue_name",
  "max_length": 1000,
  "visibility_timeout": 30
}
```

**Response (201 Created):**
```json
{
  "name": "queue_name",
  "message_count": 0,
  "max_length": 1000,
  "visibility_timeout": 30
}
```

**Error Response (409 Conflict):**
```json
{
  "detail": "Queue with the given name already exists."
}
```

---

### List All Queues

**GET** `/queues`

**Response:**
```json
{
  "queues": [
    {
      "name": "queue_name",
      "message_count": 5,
      "max_length": 1000,
      "visibility_timeout": 30
    }
  ]
}
```

---

### Update Queue Configuration

**PATCH** `/queues/{name}`

**Request Body:**
```json
{
  "max_length": 2000,
  "visibility_timeout": 60
}
```

**Response:**
```json
{
  "name": "queue_name",
  "message_count": 5,
  "max_length": 2000,
  "visibility_timeout": 60
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Queue not found."
}
```

---

### Delete Queue

**DELETE** `/queues/{name}`

**Response:** `204 No Content`

**Error Response (404 Not Found):**
```json
{
  "detail": "Queue not found."
}
```

---

## Message APIs

**Note:** All message operations require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

All message operations use a single endpoint with different request payloads based on the action.

### Send Message

**POST** `/queue/{queue_name}`

**Request Body:**
```json
{
  "Action": "SendMessage",
  "MessageBody": "Your message content here",
  "MessageAttributes": {
    "attribute1": "value1",
    "attribute2": "value2"
  }
}
```

**Response:**
```json
{
  "MessageId": "abc123",
  "status": "sent"
}
```

**Error Responses:**
- `404 Not Found`: Queue not found
- `500 Internal Server Error`: Server error

---

### Receive Messages

**POST** `/queue/{queue_name}`

**Request Body:**
```json
{
  "Action": "ReceiveMessage",
  "MaxNumberOfMessages": 1
}
```

**Response:**
```json
{
  "Messages": [
    {
      "MessageId": "abc123",
      "Body": "Your message content here",
      "Attributes": {
        "attribute1": "value1",
        "attribute2": "value2"
      },
      "ReceiptHandle": "receipt_handle_123"
    }
  ]
}
```

**Error Response:**
- `500 Internal Server Error`: Server error

---

### Delete Message

**POST** `/queue/{queue_name}`

**Request Body:**
```json
{
  "Action": "DeleteMessage",
  "ReceiptHandle": "receipt_handle_123"
}
```

**Response:**
```json
{
  "message": "Message deleted successfully"
}
```

**Error Responses:**
- `404 Not Found`: Message or queue not found
- `500 Internal Server Error`: Server error

---

## Error Handling

All endpoints follow standard HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `204 No Content`: Successful request with no response body
- `400 Bad Request`: Invalid request format or missing parameters
- `401 Unauthorized`: Authentication required or invalid credentials
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `500 Internal Server Error`: Server error

Error responses include a `detail` field with a human-readable error message.

---

## Authentication Methods

FastQueue supports two authentication methods:

1. **JWT Tokens** (Recommended): Use the `/auth/login` endpoint to get access and refresh tokens. Include the access token in the `Authorization` header as `Bearer <token>`.

2. **API Keys**: Alternative authentication method (implementation details depend on your `verify_api_key` service).

Make sure to include proper authentication headers in all requests to queue and message endpoints.