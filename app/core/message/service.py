from app.core.message.schemas import (
    SendMessageRequest,
    SendMessageResponse,
    ReceiveMessageResponse,
    DeleteMessageRequest,
)
from app.core.queue.registry import QueueRegistry


def send_message(queue_name: str, request: SendMessageRequest) -> SendMessageResponse:
    queue_manager = QueueRegistry.get_queue(queue_name)
    if not queue_manager:
        raise ValueError(f"Queue '{queue_name}' does not exist")

    response = queue_manager.send_message(request)
    return response


def receive_messages(queue_name: str, max_number: int = 1) -> ReceiveMessageResponse:
    queue_manager = QueueRegistry.get_queue(queue_name)
    if not queue_manager:
        raise ValueError(f"Queue '{queue_name}' does not exist")

    messages = queue_manager.receive_messages(max_number)
    return messages


def delete_message(queue_name: str, request: DeleteMessageRequest):
    queue_manager = QueueRegistry.get_queue(queue_name)
    if not queue_manager:
        raise ValueError(f"Queue '{queue_name}' does not exist")

    success = queue_manager.delete_message(request.ReceiptHandle)
    if not success:
        raise ValueError(
            f"ReceiptHandle '{request.ReceiptHandle}' not found or already deleted"
        )
