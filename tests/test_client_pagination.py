import httpx

from coc_api_wrapper import CoCClient


def test_get_clan_members_sends_limit_after_and_parses_cursor() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.raw_path.decode().startswith("/v1/clans/%23ABC/members")
        assert request.url.params.get("limit") == "10"
        assert request.url.params.get("after") == "cursor"
        return httpx.Response(
            200,
            json={
                "items": [{"tag": "%23P1", "name": "Member"}],
                "paging": {"cursors": {"after": "next"}},
            },
        )

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport, base_url="https://api.clashofclans.com/v1")
    client = CoCClient(token="token", client=http_client, max_retries=0)

    page = client.get_clan_members("#abc", limit=10, after="cursor")
    assert page.items[0].name == "Member"
    assert page.after == "next"
