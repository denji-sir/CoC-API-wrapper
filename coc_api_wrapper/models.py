from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class CoCBaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore")


class BadgeUrls(CoCBaseModel):
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


def ensure_object(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise TypeError(f"Expected JSON object, got {type(payload).__name__}")
    return payload

