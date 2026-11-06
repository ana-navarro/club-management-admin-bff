from dataclasses import dataclass
from typing import Any, Protocol

JsonObject = dict[str, Any]


class UpstreamError(Exception):
    """A failed call to an internal service, keeping its status and error code."""

    def __init__(self, status_code: int, code: str) -> None:
        super().__init__(code)
        self.status_code = status_code
        self.code = code


@dataclass(frozen=True)
class ClientInfo:
    ip: str | None
    user_agent: str | None


class LoginPort(Protocol):
    def __call__(self, body: JsonObject) -> JsonObject: ...


class RefreshTokenPort(Protocol):
    def __call__(self, authorization: str) -> JsonObject: ...


class ForgotPasswordPort(Protocol):
    def __call__(self, body: JsonObject) -> None: ...


class ResetPasswordPort(Protocol):
    def __call__(self, body: JsonObject) -> None: ...


class GetCurrentUserPort(Protocol):
    def __call__(self, authorization: str) -> JsonObject: ...


class UpdatePreferencesPort(Protocol):
    def __call__(self, authorization: str, body: JsonObject) -> JsonObject: ...
