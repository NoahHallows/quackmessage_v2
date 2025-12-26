from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class receiveMessagesRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: bool
    def __init__(self, request: bool = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("sender", "receiver", "content", "messageId")
    SENDER_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    sender: str
    receiver: str
    content: str
    messageId: int
    def __init__(self, sender: _Optional[str] = ..., receiver: _Optional[str] = ..., content: _Optional[str] = ..., messageId: _Optional[int] = ...) -> None: ...

class sendMessageResult(_message.Message):
    __slots__ = ("sendSuccessfull", "messageId")
    SENDSUCCESSFULL_FIELD_NUMBER: _ClassVar[int]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    sendSuccessfull: bool
    messageId: int
    def __init__(self, sendSuccessfull: bool = ..., messageId: _Optional[int] = ...) -> None: ...
