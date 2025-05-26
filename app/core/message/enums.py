from enum import Enum


class SQSAction(str, Enum):
    SendMessage = "SendMessage"
    ReceiveMessage = "ReceiveMessage"
    DeleteMessage = "DeleteMessage"
