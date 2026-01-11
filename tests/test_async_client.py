import httpx

from coc_api_wrapper import AsyncCoCClient


async def test_async_get_player_works() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.raw_path.decode() == "/v1/players/%23P"
        return httpx.Response(200, json={"tag": "%23P", "name": "Player"})

    transport = httpx.MockTransport(handler)
    http_client = httpx.AsyncClient(transport=transport, base_url="https://api.clashofclans.com/v1")
    async with AsyncCoCClient(token="token", client=http_client, max_retries=0) as client:
        player = await client.get_player("#p")
        assert player.name == "Player"
