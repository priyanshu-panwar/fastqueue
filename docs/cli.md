# FastQueue CLI Documentation

The FastQueue CLI provides a command-line interface for managing users, queues, and performing administrative tasks. This tool is particularly useful for server administration and automation scripts.

---

## Installation & Usage

### Running the CLI

The CLI can be executed using Python's module syntax:

```bash
python -m cli.main [COMMAND] [SUBCOMMAND] [OPTIONS]
```

### Docker Usage

If you're running FastQueue in a Docker container, you can execute CLI commands inside the container:

```bash
# Enter the running container
docker exec -it <container_name> bash

# Then run CLI commands
python -m cli.main auth create
python -m cli.main queue list
```

Or execute commands directly:

```bash
docker exec -it <container_name> python -m cli.main auth create
```

---

## Available Commands

The CLI is organized into two main command groups:

- **`auth`** - User authentication and management
- **`queue`** - Queue management operations

### Getting Help

```bash
# General help
python -m cli.main --help

# Help for specific command group
python -m cli.main auth --help
python -m cli.main queue --help

# Help for specific command
python -m cli.main auth create --help
```

---

## Authentication Commands

All authentication commands are under the `auth` namespace.

### Create User

Create a new user account with username and password.

**Command:**
```bash
python -m cli.main auth create
```

**Interactive Prompts:**
- `Enter username`: Your desired username
- `Enter password`: Your password (hidden input)
- `Repeat for confirmation`: Confirm your password (hidden input)

**Example:**
```bash
$ python -m cli.main auth create
Enter username: john_doe
Enter password: ********
Repeat for confirmation: ********
✅ User 'john_doe' created successfully.
```

---

### Delete User

Delete an existing user account. Requires username and password for verification.

**Command:**
```bash
python -m cli.main auth delete
```

**Interactive Prompts:**
- `Enter username`: Username to delete
- `Enter password`: Current password for verification (hidden input)

**Example:**
```bash
$ python -m cli.main auth delete
Enter username: john_doe
Enter password: ********
🗑️ User 'john_doe' deleted.
```

---

### Change Password

Change the password for an existing user account.

**Command:**
```bash
python -m cli.main auth change-password
```

**Interactive Prompts:**
- `Enter username`: Username for password change
- `Enter old password`: Current password (hidden input)
- `Enter new password`: New password (hidden input)
- `Repeat for confirmation`: Confirm new password (hidden input)

**Example:**
```bash
$ python -m cli.main auth change-password
Enter username: john_doe
Enter old password: ********
Enter new password: ********
Repeat for confirmation: ********
🔐 Password updated for user 'john_doe'.
```

---

## Queue Management Commands

All queue management commands are under the `queue` namespace.

### Create Queue

Create a new message queue.

**Command:**
```bash
python -m cli.main queue create
```

**Interactive Prompts:**
- `Enter queue name`: Name for the new queue

**Example:**
```bash
$ python -m cli.main queue create
Enter queue name: order_processing
✅ Queue 'order_processing' created successfully.
```

**Error Handling:**
- If a queue with the same name already exists, you'll see an error message and the command will exit with code 1.

```bash
$ python -m cli.main queue create
Enter queue name: existing_queue
Queue 'existing_queue' already exists.
```

---

### List Queues

Display all existing queues in a formatted table.

**Command:**
```bash
python -m cli.main queue list
```

**Example Output:**
```bash
$ python -m cli.main queue list
                    Queues                    
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name                                     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ order_processing                         │
│ user_notifications                       │
│ background_tasks                         │
└──────────────────────────────────────────┘
```

**No Queues Found:**
```bash
$ python -m cli.main queue list
No queues found.
```

---

### Delete Queue

Delete an existing queue by name.

**Command:**
```bash
python -m cli.main queue delete
```

**Interactive Prompts:**
- `Enter queue name to delete`: Name of the queue to delete

**Example:**
```bash
$ python -m cli.main queue delete
Enter queue name to delete: old_queue
🗑️ Queue 'old_queue' deleted.
```

**Error Handling:**
- If the queue doesn't exist, you'll see an error message:

```bash
$ python -m cli.main queue delete
Enter queue name to delete: nonexistent_queue
Queue 'nonexistent_queue' not found.
```

---

### Show Queue Details

Display detailed information about a specific queue.

**Command:**
```bash
python -m cli.main queue show
```

**Interactive Prompts:**
- `Enter queue name`: Name of the queue to inspect

**Example:**
```bash
$ python -m cli.main queue show
Enter queue name: order_processing
Queue: order_processing
Visibility Timeout: 30 seconds
```

**Error Handling:**
- If the queue doesn't exist:

```bash
$ python -m cli.main queue show
Enter queue name: nonexistent_queue
Queue 'nonexistent_queue' not found.
```

---

