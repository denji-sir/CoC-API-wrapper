import httpx
import pytest

from coc_api_wrapper import CoCClient
from coc_api_wrapper.exceptions import NotFound, RateLimited


def test_client_retries_on_5xx_then_succeeds() -> None:
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(500, json={"reason": "oops"})
        return httpx.Response(200, json={"tag": "%23ABC", "name": "Test Clan"})

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport, base_url="https://api.clashofclans.com/v1")
    client = CoCClient(
        token="token",
        client=http_client,
        max_retries=1,
        backoff_base=0.0,
        backoff_max=0.0,
    )

    clan = client.get_clan("#abc")
    assert clan.name == "Test Clan"
    assert calls["n"] == 2


def test_client_rate_limited_after_retries() -> None:
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(429, headers={"Retry-After": "12"}, json={"reason": "limit"})

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport, base_url="https://api.clashofclans.com/v1")
    client = CoCClient(
        token="token",
        client=http_client,
        max_retries=1,
        backoff_base=0.0,
        backoff_max=0.0,
    )

    with pytest.raises(RateLimited) as exc:
        client.get_clan("#abc")
    assert exc.value.retry_after == 12.0
    assert calls["n"] == 2


def test_client_not_found_raises() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"reason": "notFound"})

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport, base_url="https://api.clashofclans.com/v1")
    client = CoCClient(token="token", client=http_client, max_retries=0)

    with pytest.raises(NotFound):
        client.get_player("#missing")
