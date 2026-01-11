from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import urlencode


def normalize_tag(tag: str) -> str:
    raw = tag.strip()
    if not raw:
        raise ValueError("Tag is empty")

    if raw.lower().startswith("%23"):
        rest = raw[3:]
    elif raw.startswith("#"):
        rest = raw[1:]
    else:
        rest = raw

    rest = rest.strip().upper()
    if not rest:
        raise ValueError("Tag is empty")
    return f"%23{rest}"


def paginate(*, limit: int | None = None, after: str | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if limit is not None:
        if limit <= 0:
            raise ValueError("limit must be positive")
        params["limit"] = limit
    if after:
        params["after"] = after
    return params


def cache_key(method: str, path: str, params: Mapping[str, Any] | None) -> str:
    if not params:
        return f"{method.upper()} {path}"
    return f"{method.upper()} {path}?{urlencode(sorted(params.items()), doseq=True)}"


def redact_token(headers: Mapping[str, str]) -> dict[str, str]:
    redacted = dict(headers)
    for key in ("authorization", "Authorization"):
        if key in redacted:
            value = redacted[key]
            if value.lower().startswith("bearer "):
                redacted[key] = "Bearer ***"
            else:
                redacted[key] = "***"
    return redacted
