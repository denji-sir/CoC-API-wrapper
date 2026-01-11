from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class CoCBaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore")


class BadgeUrls(CoCBaseModel):
    small: str | None = None
    medium: str | None = None
    large: str | None = None


class IconUrls(CoCBaseModel):
    small: str | None = None
    medium: str | None = None
    large: str | None = None


class Clan(CoCBaseModel):
    tag: str
    name: str
    clan_level: int | None = Field(default=None, alias="clanLevel")
    members: int | None = None
    description: str | None = None
    badge_urls: BadgeUrls | None = Field(default=None, alias="badgeUrls")


class PlayerClan(CoCBaseModel):
    tag: str
    name: str
    badge_urls: BadgeUrls | None = Field(default=None, alias="badgeUrls")


class Player(CoCBaseModel):
    tag: str
    name: str
    town_hall_level: int | None = Field(default=None, alias="townHallLevel")
    exp_level: int | None = Field(default=None, alias="expLevel")
    trophies: int | None = None
    clan: PlayerClan | None = None


class ClanMember(CoCBaseModel):
    tag: str
    name: str
    role: str | None = None
    exp_level: int | None = Field(default=None, alias="expLevel")
    trophies: int | None = None


class Label(CoCBaseModel):
    id: int | None = None
    name: str | None = None
    icon_urls: IconUrls | None = Field(default=None, alias="iconUrls")


class League(CoCBaseModel):
    id: int | None = None
    name: str | None = None
    icon_urls: IconUrls | None = Field(default=None, alias="iconUrls")


class Location(CoCBaseModel):
    id: int | None = None
    name: str | None = None
    is_country: bool | None = Field(default=None, alias="isCountry")
    country_code: str | None = Field(default=None, alias="countryCode")


class Cursors(CoCBaseModel):
    after: str | None = None
    before: str | None = None


class Paging(CoCBaseModel):
    cursors: Cursors | None = None


T = TypeVar("T")


class Page(CoCBaseModel, Generic[T]):
    items: list[T]
    paging: Paging | None = None

    @property
    def after(self) -> str | None:
        return self.paging.cursors.after if (self.paging and self.paging.cursors) else None


class ClanMembersPage(Page[ClanMember]):
    items: list[ClanMember]


class Season(CoCBaseModel):
    id: str | None = None


class Ranking(CoCBaseModel):
    rank: int | None = None
    previous_rank: int | None = Field(default=None, alias="previousRank")


class WarMember(CoCBaseModel):
    tag: str | None = None
    name: str | None = None


class WarClan(CoCBaseModel):
    tag: str | None = None
    name: str | None = None
    badge_urls: BadgeUrls | None = Field(default=None, alias="badgeUrls")
    clan_level: int | None = Field(default=None, alias="clanLevel")
    attacks: int | None = None
    stars: int | None = None
    destruction_percentage: float | None = Field(default=None, alias="destructionPercentage")


class CurrentWar(CoCBaseModel):
    state: str | None = None
    team_size: int | None = Field(default=None, alias="teamSize")
    start_time: str | None = Field(default=None, alias="startTime")
    end_time: str | None = Field(default=None, alias="endTime")
    clan: WarClan | None = None
    opponent: WarClan | None = None


class WarLogClan(WarClan):
    pass


class WarLogEntry(CoCBaseModel):
    result: str | None = None
    end_time: str | None = Field(default=None, alias="endTime")
    team_size: int | None = Field(default=None, alias="teamSize")
    attacks_per_member: int | None = Field(default=None, alias="attacksPerMember")
    clan: WarLogClan | None = None
    opponent: WarLogClan | None = None


class WarLogPage(Page[WarLogEntry]):
    items: list[WarLogEntry]


class CWLClan(CoCBaseModel):
    tag: str | None = None
    name: str | None = None
    badge_urls: BadgeUrls | None = Field(default=None, alias="badgeUrls")
    clan_level: int | None = Field(default=None, alias="clanLevel")


class CWLRound(CoCBaseModel):
    war_tags: list[str] | None = Field(default=None, alias="warTags")


class CWLLeagueGroup(CoCBaseModel):
    tag: str | None = None
    state: str | None = None
    season: str | None = None
    clans: list[CWLClan] | None = None
    rounds: list[CWLRound] | None = None


class CWLWarMember(WarMember):
    town_hall_level: int | None = Field(default=None, alias="townHallLevel")
    map_position: int | None = Field(default=None, alias="mapPosition")


class CWLWarClan(CoCBaseModel):
    tag: str | None = None
    name: str | None = None
    badge_urls: BadgeUrls | None = Field(default=None, alias="badgeUrls")
    clan_level: int | None = Field(default=None, alias="clanLevel")
    attacks: int | None = None
    stars: int | None = None
    destruction_percentage: float | None = Field(default=None, alias="destructionPercentage")
    members: list[CWLWarMember] | None = None


class CWLWar(CoCBaseModel):
    state: str | None = None
    team_size: int | None = Field(default=None, alias="teamSize")
    start_time: str | None = Field(default=None, alias="startTime")
    end_time: str | None = Field(default=None, alias="endTime")
    clan: CWLWarClan | None = None
    opponent: CWLWarClan | None = None


class RaidSeason(CoCBaseModel):
    state: str | None = None
    start_time: str | None = Field(default=None, alias="startTime")
    end_time: str | None = Field(default=None, alias="endTime")
    capital_total_loot: int | None = Field(default=None, alias="capitalTotalLoot")
    raids_completed: int | None = Field(default=None, alias="raidsCompleted")
    total_attacks: int | None = Field(default=None, alias="totalAttacks")
    enemy_districts_destroyed: int | None = Field(default=None, alias="enemyDistrictsDestroyed")
    offensive_reward: int | None = Field(default=None, alias="offensiveReward")
    defensive_reward: int | None = Field(default=None, alias="defensiveReward")


class RaidSeasonsPage(Page[RaidSeason]):
    items: list[RaidSeason]


class ClanRanking(Ranking):
    tag: str | None = None
    name: str | None = None
    clan_level: int | None = Field(default=None, alias="clanLevel")
    members: int | None = None
    clan_points: int | None = Field(default=None, alias="clanPoints")
    capital_points: int | None = Field(default=None, alias="capitalPoints")
    badge_urls: BadgeUrls | None = Field(default=None, alias="badgeUrls")


class PlayerRanking(Ranking):
    tag: str | None = None
    name: str | None = None
    exp_level: int | None = Field(default=None, alias="expLevel")
    trophies: int | None = None
    clan: PlayerClan | None = None


class CapitalRanking(Ranking):
    tag: str | None = None
    name: str | None = None
    clan_level: int | None = Field(default=None, alias="clanLevel")
    capital_points: int | None = Field(default=None, alias="capitalPoints")
    badge_urls: BadgeUrls | None = Field(default=None, alias="badgeUrls")


class LeagueSeason(Season):
    pass


class LeagueSeasonRank(Ranking):
    tag: str | None = None
    name: str | None = None
    trophies: int | None = None
    clan: PlayerClan | None = None


class GoldPassSeason(CoCBaseModel):
    start_time: str | None = Field(default=None, alias="startTime")
    end_time: str | None = Field(default=None, alias="endTime")


class ClanLabelsPage(Page[Label]):
    items: list[Label]


class CWLLeaguePage(Page[League]):
    items: list[League]


class LocationsPage(Page[Location]):
    items: list[Location]


class ClanRankingPage(Page[ClanRanking]):
    items: list[ClanRanking]


class PlayerRankingPage(Page[PlayerRanking]):
    items: list[PlayerRanking]


class CapitalRankingPage(Page[CapitalRanking]):
    items: list[CapitalRanking]


class LeaguesPage(Page[League]):
    items: list[League]


class LeagueSeasonsPage(Page[LeagueSeason]):
    items: list[LeagueSeason]


class LeagueSeasonRankingsPage(Page[LeagueSeasonRank]):
    items: list[LeagueSeasonRank]


def ensure_object(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise TypeError(f"Expected JSON object, got {type(payload).__name__}")
    return payload
