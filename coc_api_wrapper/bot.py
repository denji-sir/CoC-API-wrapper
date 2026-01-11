from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Generic, Literal, TypeVar

from .exceptions import APIError, NotFound, RateLimited, ServerError, Unauthorized

BotErrorKind = Literal["unauthorized", "not_found", "rate_limited", "server_error", "api_error"]


@dataclass(frozen=True, slots=True)
class BotError:
    kind: BotErrorKind
    message: str
    retry_after: float | None = None


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class BotResult(Generic[T]):
    value: T | None = None
    error: BotError | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


def bot_error_from_exception(exc: Exception) -> BotError:
    if isinstance(exc, Unauthorized):
        return BotError(kind="unauthorized", message="Нужен валидный API токен (Unauthorized).")
    if isinstance(exc, NotFound):
        return BotError(kind="not_found", message="Ничего не найдено по этому тегу.")
    if isinstance(exc, RateLimited):
        return BotError(
            kind="rate_limited",
            message="Слишком много запросов (rate limit).",
            retry_after=exc.retry_after,
        )
    if isinstance(exc, ServerError):
        return BotError(kind="server_error", message="Проблема на стороне CoC API. Попробуй позже.")
    if isinstance(exc, APIError):
        return BotError(kind="api_error", message="Ошибка CoC API.")
    return BotError(kind="api_error", message="Неизвестная ошибка.")


def format_bot_error(error: BotError) -> str:
    if error.kind == "rate_limited" and error.retry_after is not None:
        seconds = int(error.retry_after)
        return f"{error.message} Попробуй через ~{seconds}s."
    return error.message


def safe_call(fn: Callable[[], T]) -> BotResult[T]:
    try:
        return BotResult(value=fn())
    except Exception as exc:
        return BotResult(error=bot_error_from_exception(exc))


async def safe_await(awaitable: Awaitable[T]) -> BotResult[T]:
    try:
        return BotResult(value=await awaitable)
    except Exception as exc:
        return BotResult(error=bot_error_from_exception(exc))


def safe_call_with_retry(
    fn: Callable[[], T],
    *,
    max_retries: int = 1,
    max_wait: float = 15.0,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> BotResult[T]:
    retries = max(0, int(max_retries))
    max_wait_seconds = float(max_wait)
    attempt = 0
    while True:
        try:
            return BotResult(value=fn())
        except RateLimited as exc:
            if attempt >= retries:
                return BotResult(error=bot_error_from_exception(exc))
            retry_after = exc.retry_after
            if retry_after is None or retry_after > max_wait_seconds:
                return BotResult(error=bot_error_from_exception(exc))
            attempt += 1
            sleep_fn(retry_after)
            continue
        except Exception as exc:
            return BotResult(error=bot_error_from_exception(exc))


async def safe_await_with_retry(
    factory: Callable[[], Awaitable[T]],
    *,
    max_retries: int = 1,
    max_wait: float = 15.0,
    sleep_fn: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> BotResult[T]:
    retries = max(0, int(max_retries))
    max_wait_seconds = float(max_wait)
    attempt = 0
    while True:
        try:
            return BotResult(value=await factory())
        except RateLimited as exc:
            if attempt >= retries:
                return BotResult(error=bot_error_from_exception(exc))
            retry_after = exc.retry_after
            if retry_after is None or retry_after > max_wait_seconds:
                return BotResult(error=bot_error_from_exception(exc))
            attempt += 1
            await sleep_fn(retry_after)
            continue
        except Exception as exc:
            return BotResult(error=bot_error_from_exception(exc))
