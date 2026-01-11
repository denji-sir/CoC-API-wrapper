from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class APIError(Exception):
    message: str
    status_code: int | None = None
    method: str | None = None
    url: str | None = None
    payload: Any | None = None

    def __str__(self) -> str:
        bits: list[str] = [self.message]
        if self.status_code is not None:
            bits.append(f"status={self.status_code}")
        if self.method and self.url:
            bits.append(f"{self.method} {self.url}")
        return " | ".join(bits)


class Unauthorized(APIError):
    pass


class NotFound(APIError):
    pass


@dataclass(frozen=True, slots=True)
class RateLimited(APIError):
    retry_after: float | None = None


class ServerError(APIError):
    pass
