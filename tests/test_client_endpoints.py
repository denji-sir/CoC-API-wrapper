import httpx

from coc_api_wrapper import CoCClient


def test_get_clan_warlog_uses_pagination() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.raw_path.decode().startswith("/v1/clans/%23ABC/warlog")
        assert request.url.params.get("limit") == "10"
        assert request.url.params.get("after") == "cursor"
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "result": "win",
                        "endTime": "20240101T000000.000Z",
                        "teamSize": 15,
                        "attacksPerMember": 2,
                        "clan": {"tag": "%23ABC", "name": "A", "clanLevel": 10},
                        "opponent": {"tag": "%23DEF", "name": "B", "clanLevel": 9},
                    }
                ],
                "paging": {"cursors": {"after": "next"}},
            },
        )

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport, base_url="https://api.clashofclans.com/v1")
    client = CoCClient(token="token", client=http_client, max_retries=0)

    page = client.get_clan_warlog("#abc", limit=10, after="cursor")
    assert page.items[0].clan is not None
    assert page.items[0].clan.name == "A"
    assert page.after == "next"


def test_get_cwl_leagues_and_war() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/clanwarleagues/warleagues":
            return httpx.Response(
                200,
                json={"items": [{"id": 48000000, "name": "CWL", "iconUrls": {}}]},
            )
        if request.url.raw_path.decode() == "/v1/clanwarleagues/wars/%23WAR":
            return httpx.Response(
                200,
                json={
                    "state": "inWar",
                    "teamSize": 15,
                    "clan": {
                        "tag": "%23A",
                        "name": "Alpha",
                        "members": [
                            {"tag": "%23P", "name": "Player", "townHallLevel": 12, "mapPosition": 1}
                        ],
                    },
                    "opponent": {"tag": "%23B", "name": "Beta", "members": []},
                },
            )
        raise AssertionError(f"Unexpected path: {request.url.path}")

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport, base_url="https://api.clashofclans.com/v1")
    client = CoCClient(token="token", client=http_client, max_retries=0)

    leagues = client.get_cwl_leagues()
    assert leagues.items[0].name == "CWL"

    war = client.get_cwl_war("#war")
    assert war.clan is not None
    assert war.clan.members is not None
    assert war.clan.members[0].name == "Player"


def test_get_locations_and_rankings() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/locations":
            return httpx.Response(
                200,
                json={
                    "items": [
                        {"id": 32000007, "name": "USA", "isCountry": True, "countryCode": "US"}
                    ]
                },
            )
        if request.url.path == "/v1/locations/32000007/rankings/clans":
            return httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "tag": "%23ABC",
                            "name": "Clan",
                            "rank": 1,
                            "previousRank": 2,
                            "clanLevel": 10,
                            "members": 50,
                            "clanPoints": 12345,
                            "badgeUrls": {},
                        }
                    ]
                },
            )
        if request.url.path == "/v1/locations/32000007/rankings/players":
            return httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "tag": "%23P",
                            "name": "Player",
                            "rank": 1,
                            "previousRank": 2,
                            "expLevel": 200,
                            "trophies": 5000,
                            "clan": {"tag": "%23C", "name": "Clan"},
                        }
                    ]
                },
            )
        if request.url.path == "/v1/locations/32000007/rankings/capital":
            return httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "tag": "%23C",
                            "name": "Clan",
                            "rank": 1,
                            "previousRank": 2,
                            "clanLevel": 10,
                            "capitalPoints": 9999,
                            "badgeUrls": {},
                        }
                    ]
                },
            )
        raise AssertionError(f"Unexpected path: {request.url.path}")

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport, base_url="https://api.clashofclans.com/v1")
    client = CoCClient(token="token", client=http_client, max_retries=0)

    locations = client.get_locations()
    assert locations.items[0].name == "USA"

    clan_rankings = client.get_location_clan_rankings(32000007)
    assert clan_rankings.items[0].name == "Clan"

    player_rankings = client.get_location_player_rankings(32000007)
    assert player_rankings.items[0].name == "Player"

    capital_rankings = client.get_location_capital_rankings(32000007)
    assert capital_rankings.items[0].name == "Clan"


def test_get_leagues_and_seasons() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/leagues":
            return httpx.Response(
                200,
                json={"items": [{"id": 20000000, "name": "Legend League", "iconUrls": {}}]},
            )
        if request.url.path == "/v1/leagues/20000000/seasons":
            return httpx.Response(200, json={"items": [{"id": "2024-01"}]})
        if request.url.path == "/v1/leagues/20000000/seasons/2024-01":
            return httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "tag": "%23P",
                            "name": "Player",
                            "rank": 1,
                            "previousRank": 2,
                            "trophies": 5000,
                            "clan": {"tag": "%23C", "name": "Clan"},
                        }
                    ]
                },
            )
        raise AssertionError(f"Unexpected path: {request.url.path}")

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport, base_url="https://api.clashofclans.com/v1")
    client = CoCClient(token="token", client=http_client, max_retries=0)

    leagues = client.get_leagues()
    assert leagues.items[0].name == "Legend League"

    seasons = client.get_league_seasons(20000000)
    assert seasons.items[0].id == "2024-01"

    rankings = client.get_league_season(20000000, "2024-01")
    assert rankings.items[0].name == "Player"


def test_get_clan_labels_and_goldpass() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/labels/clans":
            return httpx.Response(
                200,
                json={"items": [{"id": 57000000, "name": "Label", "iconUrls": {}}]},
            )
        if request.url.path == "/v1/goldpass/seasons/current":
            return httpx.Response(
                200,
                json={"startTime": "20240101T000000.000Z", "endTime": "20240131T000000.000Z"},
            )
        raise AssertionError(f"Unexpected path: {request.url.path}")

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport, base_url="https://api.clashofclans.com/v1")
    client = CoCClient(token="token", client=http_client, max_retries=0)

    labels = client.get_clan_labels()
    assert labels.items[0].name == "Label"

    goldpass = client.get_current_goldpass()
    assert goldpass.start_time == "20240101T000000.000Z"
