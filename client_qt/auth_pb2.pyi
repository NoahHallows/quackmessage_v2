from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ClientVersion(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: float
    def __init__(self, version: _Optional[float] = ...) -> None: ...

class ValidVersion(_message.Message):
    __slots__ = ("valid", "valid_version_num")
    VALID_FIELD_NUMBER: _ClassVar[int]
    VALID_VERSION_NUM_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    valid_version_num: float
    def __init__(self, valid: bool = ..., valid_version_num: _Optional[float] = ...) -> None: ...

class LoginMessage(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class LoginResult(_message.Message):
    __slots__ = ("success", "auth_token")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    success: bool
    auth_token: str
    def __init__(self, success: bool = ..., auth_token: _Optional[str] = ...) -> None: ...

class VerifyEmailMessage(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class VerificationEmailSent(_message.Message):
    __slots__ = ("emailSent",)
    EMAILSENT_FIELD_NUMBER: _ClassVar[int]
    emailSent: bool
    def __init__(self, emailSent: bool = ...) -> None: ...

class VerificationCodeMessage(_message.Message):
    __slots__ = ("code", "email")
    CODE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    code: int
    email: str
    def __init__(self, code: _Optional[int] = ..., email: _Optional[str] = ...) -> None: ...

class VerificationCodeMatches(_message.Message):
    __slots__ = ("verified",)
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    verified: bool
    def __init__(self, verified: bool = ...) -> None: ...

class CreateUserMessage(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class CreateUserResult(_message.Message):
    __slots__ = ("success", "auth_token")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    success: bool
    auth_token: str
    def __init__(self, success: bool = ..., auth_token: _Optional[str] = ...) -> None: ...
