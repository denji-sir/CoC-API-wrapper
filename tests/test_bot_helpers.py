import httpx
import pytest

from coc_api_wrapper import (
    AsyncCoCClient,
    BotError,
    format_bot_error,
    safe_await,
    safe_await_with_retry,
)


async def test_safe_await_turns_exception_into_bot_error_message() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, headers={"Retry-After": "5"}, json={"reason": "limit"})

    transport = httpx.MockTransport(handler)
    http_client = httpx.AsyncClient(transport=transport, base_url="https://api.clashofclans.com/v1")
    async with AsyncCoCClient(
        token="token",
        client=http_client,
        max_retries=0,
    ) as client:
        result = await safe_await(client.get_player("#P"))
        assert not result.ok
        assert result.error is not None
        assert "5s" in format_bot_error(result.error, locale="ru")


async def test_safe_await_with_retry_waits_for_retry_after() -> None:
    calls = {"n": 0, "slept": []}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(429, headers={"Retry-After": "2"}, json={"reason": "limit"})
        return httpx.Response(200, json={"tag": "%23P", "name": "Player"})

    async def sleep_fn(seconds: float) -> None:
        calls["slept"].append(seconds)

    transport = httpx.MockTransport(handler)
    http_client = httpx.AsyncClient(transport=transport, base_url="https://api.clashofclans.com/v1")
    async with AsyncCoCClient(
        token="token",
        client=http_client,
        max_retries=0,
    ) as client:
        result = await safe_await_with_retry(
            lambda: client.get_player("#P"),
            max_retries=1,
            sleep_fn=sleep_fn,
        )
        assert result.ok
        assert result.value is not None
        assert result.value.name == "Player"
        assert calls["slept"] == [2.0]


def test_format_bot_error_locale_override() -> None:
    error = BotError(kind="unauthorized")
    assert format_bot_error(error, locale="en") == "A valid API token is required (Unauthorized)."
    assert format_bot_error(error, locale="ru") == "Нужен валидный API токен (Unauthorized)."


def test_format_bot_error_uses_env_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_LOCALE", "en")
    error = BotError(kind="not_found")
    assert format_bot_error(error) == "Nothing found for this tag."
