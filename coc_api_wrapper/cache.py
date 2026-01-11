from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

V = TypeVar("V")


@dataclass(slots=True)
class _CacheItem(Generic[V]):
    expires_at: float
    value: V


class TTLCache(Generic[V]):
    def __init__(
        self,
        *,
        enabled: bool = True,
        default_ttl: float = 30.0,
        time_fn: Callable[[], float] = time.monotonic,
    ) -> None:
        self._enabled = enabled
        self._default_ttl = float(default_ttl)
        self._time_fn = time_fn
        self._items: dict[str, _CacheItem[V]] = {}

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = bool(value)
        if not self._enabled:
            self._items.clear()

    @property
    def default_ttl(self) -> float:
        return self._default_ttl

    def clear(self) -> None:
        self._items.clear()

    def get(self, key: str) -> V | None:
        if not self._enabled:
            return None
        item = self._items.get(key)
        if item is None:
            return None
        if item.expires_at <= self._time_fn():
            self._items.pop(key, None)
            return None
        return item.value

    def set(self, key: str, value: V, *, ttl: float | None = None) -> None:
        if not self._enabled:
            return
        ttl_value = self._default_ttl if ttl is None else float(ttl)
        if ttl_value <= 0:
            return
        self._items[key] = _CacheItem(expires_at=self._time_fn() + ttl_value, value=value)
