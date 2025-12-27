from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

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
    __slots__ = ("sendSuccessful", "message_id")
    SENDSUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    sendSuccessful: bool
    message_id: int
    def __init__(self, sendSuccessful: bool = ..., message_id: _Optional[int] = ...) -> None: ...

class contactsRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: bool
    def __init__(self, request: bool = ...) -> None: ...

class contact(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class contactList(_message.Message):
    __slots__ = ("contacts",)
    CONTACTS_FIELD_NUMBER: _ClassVar[int]
    contacts: _containers.RepeatedCompositeFieldContainer[contact]
    def __init__(self, contacts: _Optional[_Iterable[_Union[contact, _Mapping]]] = ...) -> None: ...
