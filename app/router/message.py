import logging
from fastapi import APIRouter, HTTPException, Depends

from app.core.message.schemas import (
    SendMessageRequest,
    ReceiveMessageRequest,
    DeleteMessageRequest,
)
from app.core.message.service import send_message, receive_messages, delete_message
from app.core.message.enums import SQSAction
from app.auth.service import verify_api_key

router = APIRouter(
    prefix="/queue", tags=["messages"], dependencies=[Depends(verify_api_key)]
)
_logger = logging.getLogger(__name__)


@router.post("/{queue_name}")
async def messages_action_runner(
    queue_name: str,
    request: SendMessageRequest | ReceiveMessageRequest | DeleteMessageRequest,
):
    if request.Action == SQSAction.SendMessage:
        try:
            return send_message(queue_name, request)
        except ValueError as e:
            _logger.error(f"Queue {queue_name} not found: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            _logger.error(f"Error sending message to queue {queue_name}: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    elif request.Action == SQSAction.ReceiveMessage:
        try:
            return receive_messages(queue_name, request.MaxNumberOfMessages)
        except Exception as e:
            _logger.error(f"Error receiving messages from queue {queue_name}: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    elif request.Action == SQSAction.DeleteMessage:
        try:
            delete_message(queue_name, request)
            return {"message": "Message deleted successfully"}
        except ValueError as e:
            _logger.error(f"Error deleting message from queue {queue_name}: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            _logger.error(f"Error deleting message from queue {queue_name}: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    else:
        raise HTTPException(status_code=400, detail="Invalid Action")
