from __future__ import annotations

import json
import logging
import time
from collections.abc import Callable, Mapping
from typing import Any

import httpx

from .cache import TTLCache
from .exceptions import APIError, NotFound, RateLimited, ServerError, Unauthorized
from .models import (
    CapitalRankingPage,
    Clan,
    ClanLabelsPage,
    ClanMembersPage,
    ClanRankingPage,
    CurrentWar,
    CWLLeagueGroup,
    CWLLeaguePage,
    CWLWar,
    GoldPassSeason,
    LeagueSeasonRankingsPage,
    LeagueSeasonsPage,
    LeaguesPage,
    LocationsPage,
    Player,
    PlayerRankingPage,
    RaidSeasonsPage,
    WarLogPage,
    ensure_object,
)
from .utils import cache_key, normalize_tag, paginate, redact_token


class CoCClient:
    def __init__(
        self,
        token: str,
        *,
        base_url: str = "https://api.clashofclans.com/v1",
        timeout: float = 10.0,
        max_retries: int = 3,
        backoff_base: float = 0.5,
        backoff_max: float = 8.0,
        cache_enabled: bool = True,
        cache_ttl: float = 30.0,
        client: httpx.Client | None = None,
        sleep_fn: Callable[[float], None] = time.sleep,
        logger: logging.Logger | None = None,
    ) -> None:
        token = token.strip()
        if not token:
            raise ValueError("token is required")

        self._base_url = base_url.rstrip("/")
        self._timeout = float(timeout)
        self._max_retries = int(max_retries)
        self._backoff_base = float(backoff_base)
        self._backoff_max = float(backoff_max)
        self._sleep = sleep_fn
        self._logger = logger or logging.getLogger("coc_api_wrapper")
        self._cache: TTLCache[dict[str, Any]] = TTLCache(
            enabled=cache_enabled,
            default_ttl=cache_ttl,
        )

        default_headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        if client is not None:
            client.headers.update(default_headers)
            self._client = client
        else:
            self._client = httpx.Client(
                base_url=self._base_url,
                timeout=httpx.Timeout(self._timeout),
                headers=default_headers,
            )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> CoCClient:
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.close()

    def get_clan(self, tag: str) -> Clan:
        payload = self._request("GET", f"/clans/{normalize_tag(tag)}")
        return Clan.model_validate(payload)

    def get_clan_members(
        self,
        tag: str,
        *,
        limit: int | None = None,
        after: str | None = None,
    ) -> ClanMembersPage:
        payload = self._request(
            "GET",
            f"/clans/{normalize_tag(tag)}/members",
            params=paginate(limit=limit, after=after),
        )
        return ClanMembersPage.model_validate(payload)

    def get_player(self, tag: str) -> Player:
        payload = self._request("GET", f"/players/{normalize_tag(tag)}")
        return Player.model_validate(payload)

    def get_current_war(self, clan_tag: str) -> CurrentWar:
        payload = self._request("GET", f"/clans/{normalize_tag(clan_tag)}/currentwar")
        return CurrentWar.model_validate(payload)

    def get_capital_raids(
        self,
        clan_tag: str,
        *,
        limit: int | None = None,
        after: str | None = None,
    ) -> RaidSeasonsPage:
        payload = self._request(
            "GET",
            f"/clans/{normalize_tag(clan_tag)}/capitalraidseasons",
            params=paginate(limit=limit, after=after),
        )
        return RaidSeasonsPage.model_validate(payload)

    def get_cwl_group(self, clan_tag: str) -> dict[str, Any]:
        payload = self._request(
            "GET",
            f"/clans/{normalize_tag(clan_tag)}/currentwar/leaguegroup",
        )
        return CWLLeagueGroup.model_validate(payload)

    def get_clan_warlog(
        self,
        tag: str,
        *,
        limit: int | None = None,
        after: str | None = None,
    ) -> WarLogPage:
        payload = self._request(
            "GET",
            f"/clans/{normalize_tag(tag)}/warlog",
            params=paginate(limit=limit, after=after),
        )
        return WarLogPage.model_validate(payload)

    def get_cwl_leagues(
        self,
        *,
        limit: int | None = None,
        after: str | None = None,
    ) -> CWLLeaguePage:
        payload = self._request(
            "GET",
            "/clanwarleagues/warleagues",
            params=paginate(limit=limit, after=after),
        )
        return CWLLeaguePage.model_validate(payload)

    def get_cwl_war(self, war_tag: str) -> CWLWar:
        payload = self._request("GET", f"/clanwarleagues/wars/{normalize_tag(war_tag)}")
        return CWLWar.model_validate(payload)

    def get_locations(
        self,
        *,
        limit: int | None = None,
        after: str | None = None,
    ) -> LocationsPage:
        payload = self._request("GET", "/locations", params=paginate(limit=limit, after=after))
        return LocationsPage.model_validate(payload)

    def get_location_clan_rankings(
        self,
        location_id: int | str,
        *,
        limit: int | None = None,
        after: str | None = None,
    ) -> ClanRankingPage:
        payload = self._request(
            "GET",
            f"/locations/{location_id}/rankings/clans",
            params=paginate(limit=limit, after=after),
        )
        return ClanRankingPage.model_validate(payload)

    def get_location_player_rankings(
        self,
        location_id: int | str,
        *,
        limit: int | None = None,
        after: str | None = None,
    ) -> PlayerRankingPage:
        payload = self._request(
            "GET",
            f"/locations/{location_id}/rankings/players",
            params=paginate(limit=limit, after=after),
        )
        return PlayerRankingPage.model_validate(payload)

    def get_location_capital_rankings(
        self,
        location_id: int | str,
        *,
        limit: int | None = None,
        after: str | None = None,
    ) -> CapitalRankingPage:
        payload = self._request(
            "GET",
            f"/locations/{location_id}/rankings/capital",
            params=paginate(limit=limit, after=after),
        )
        return CapitalRankingPage.model_validate(payload)

    def get_leagues(
        self,
        *,
        limit: int | None = None,
        after: str | None = None,
    ) -> LeaguesPage:
        payload = self._request("GET", "/leagues", params=paginate(limit=limit, after=after))
        return LeaguesPage.model_validate(payload)

    def get_league_seasons(
        self,
        league_id: int | str,
        *,
        limit: int | None = None,
        after: str | None = None,
    ) -> LeagueSeasonsPage:
        payload = self._request(
            "GET",
            f"/leagues/{league_id}/seasons",
            params=paginate(limit=limit, after=after),
        )
        return LeagueSeasonsPage.model_validate(payload)

    def get_league_season(
        self,
        league_id: int | str,
        season_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
    ) -> LeagueSeasonRankingsPage:
        payload = self._request(
            "GET",
            f"/leagues/{league_id}/seasons/{season_id}",
            params=paginate(limit=limit, after=after),
        )
        return LeagueSeasonRankingsPage.model_validate(payload)

    def get_clan_labels(
        self,
        *,
        limit: int | None = None,
        after: str | None = None,
    ) -> ClanLabelsPage:
        payload = self._request(
            "GET",
            "/labels/clans",
            params=paginate(limit=limit, after=after),
        )
        return ClanLabelsPage.model_validate(payload)

    def get_current_goldpass(self) -> GoldPassSeason:
        payload = self._request("GET", "/goldpass/seasons/current")
        return GoldPassSeason.model_validate(payload)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        method_upper = method.upper()
        key = cache_key(method_upper, path, params)
        if method_upper == "GET":
            cached = self._cache.get(key)
            if cached is not None:
                return cached

        url_for_logs = f"{self._base_url}{path}"
        headers_for_logs = redact_token(self._client.headers)

        last_response: httpx.Response | None = None
        for attempt in range(self._max_retries + 1):
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug(
                    "request attempt=%s %s %s params=%s headers=%s",
                    attempt + 1,
                    method_upper,
                    url_for_logs,
                    dict(params) if params else None,
                    headers_for_logs,
                )
            try:
                response = self._client.request(method_upper, path, params=params)
                last_response = response
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                if attempt >= self._max_retries:
                    raise APIError(
                        "Request failed",
                        method=method_upper,
                        url=url_for_logs,
                        payload=str(exc),
                    ) from exc
                self._sleep(self._backoff(attempt))
                continue

            if response.status_code == 200:
                payload = ensure_object(self._parse_json(response, url_for_logs, method_upper))
                if method_upper == "GET":
                    self._cache.set(key, payload)
                return payload

            if response.status_code in (401, 403):
                raise Unauthorized(
                    "Unauthorized",
                    status_code=response.status_code,
                    method=method_upper,
                    url=url_for_logs,
                    payload=self._safe_payload(response),
                )
            if response.status_code == 404:
                raise NotFound(
                    "Not found",
                    status_code=response.status_code,
                    method=method_upper,
                    url=url_for_logs,
                    payload=self._safe_payload(response),
                )

            if response.status_code == 429:
                retry_after = self._retry_after_seconds(response.headers)
                if attempt >= self._max_retries:
                    raise RateLimited(
                        "Rate limited",
                        status_code=response.status_code,
                        method=method_upper,
                        url=url_for_logs,
                        payload=self._safe_payload(response),
                        retry_after=retry_after,
                    )
                self._sleep(max(retry_after or 0.0, self._backoff(attempt)))
                continue

            if 500 <= response.status_code <= 599:
                if attempt >= self._max_retries:
                    raise ServerError(
                        "Server error",
                        status_code=response.status_code,
                        method=method_upper,
                        url=url_for_logs,
                        payload=self._safe_payload(response),
                    )
                self._sleep(self._backoff(attempt))
                continue

            raise APIError(
                "API error",
                status_code=response.status_code,
                method=method_upper,
                url=url_for_logs,
                payload=self._safe_payload(response),
            )

        raise APIError(
            "Request failed",
            status_code=last_response.status_code if last_response else None,
            method=method_upper,
            url=url_for_logs,
        )

    def _backoff(self, attempt: int) -> float:
        delay = self._backoff_base * (2**attempt)
        return min(delay, self._backoff_max)

    @staticmethod
    def _retry_after_seconds(headers: Mapping[str, str]) -> float | None:
        value = headers.get("Retry-After")
        if not value:
            return None
        try:
            return float(value)
        except ValueError:
            return None

    @staticmethod
    def _parse_json(response: httpx.Response, url: str, method: str) -> Any:
        if response.status_code == 204:
            return {}
        try:
            return response.json()
        except (ValueError, json.JSONDecodeError) as exc:
            raise APIError(
                "Invalid JSON response",
                status_code=response.status_code,
                method=method,
                url=url,
                payload=response.text,
            ) from exc

    @staticmethod
    def _safe_payload(response: httpx.Response) -> Any:
        try:
            return response.json()
        except Exception:
            return response.text
