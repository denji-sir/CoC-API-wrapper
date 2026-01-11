## Методы и пути (MVP + top-15)

### Уже есть (MVP)
- `get_clan(tag)` -> `GET /clans/{tag}` -> `Clan`
- `get_clan_members(tag, limit=None, after=None)` -> `GET /clans/{tag}/members` -> `ClanMembersPage`
- `get_player(tag)` -> `GET /players/{tag}` -> `Player`
- `get_current_war(clan_tag)` -> `GET /clans/{tag}/currentwar` -> `CurrentWar`
- `get_capital_raids(clan_tag, limit=None, after=None)` -> `GET /clans/{tag}/capitalraidseasons` -> `RaidSeasonsPage`
- `get_cwl_group(clan_tag)` -> `GET /clans/{tag}/currentwar/leaguegroup` -> `CWLLeagueGroup`

### Добавляем (top-15)
- `get_clan_warlog(tag, limit=None, after=None)` -> `GET /clans/{tag}/warlog` -> `WarLogPage`
- `get_cwl_leagues()` -> `GET /clanwarleagues/warleagues` -> `CWLLeaguePage`
- `get_cwl_war(war_tag)` -> `GET /clanwarleagues/wars/{warTag}` -> `CWLWar`
- `get_locations(limit=None, after=None)` -> `GET /locations` -> `LocationsPage`
- `get_location_clan_rankings(location_id, limit=None, after=None)` -> `GET /locations/{id}/rankings/clans` -> `ClanRankingPage`
- `get_location_player_rankings(location_id, limit=None, after=None)` -> `GET /locations/{id}/rankings/players` -> `PlayerRankingPage`
- `get_location_capital_rankings(location_id, limit=None, after=None)` -> `GET /locations/{id}/rankings/capital` -> `CapitalRankingPage`
- `get_leagues(limit=None, after=None)` -> `GET /leagues` -> `LeaguesPage`
- `get_league_seasons(league_id, limit=None, after=None)` -> `GET /leagues/{id}/seasons` -> `LeagueSeasonsPage`
- `get_league_season(league_id, season_id, limit=None, after=None)` -> `GET /leagues/{id}/seasons/{seasonId}` -> `LeagueSeasonRankingsPage`
- `get_clan_labels(limit=None, after=None)` -> `GET /labels/clans` -> `ClanLabelsPage`
- `get_current_goldpass()` -> `GET /goldpass/seasons/current` -> `GoldPassSeason`

## Минимальные поля для моделей (с нормальными вложенностями)

### Общие сущности
- `IconUrls`: `small`, `medium`, `large`
- `Label`: `id`, `name`, `iconUrls`
- `League`: `id`, `name`, `iconUrls`
- `Location`: `id`, `name`, `isCountry`, `countryCode`

### War Log
- `WarLogEntry`: `result`, `endTime`, `teamSize`, `attacksPerMember`, `clan`, `opponent`
- `WarLogClan`: `tag`, `name`, `badgeUrls`, `clanLevel`, `stars`, `destructionPercentage`, `attacks`
- `WarLogPage`: `items`, `paging`

### CWL LeagueGroup
- `CWLLeagueGroup`: `tag`, `state`, `season`, `clans`, `rounds`
- `CWLClan`: `tag`, `name`, `badgeUrls`, `clanLevel`
- `CWLRound`: `warTags`

### CWL War
- `CWLWar`: `state`, `teamSize`, `startTime`, `endTime`, `clan`, `opponent`
- `CWLWarClan`: `tag`, `name`, `badgeUrls`, `clanLevel`, `stars`, `destructionPercentage`, `attacks`, `members`
- `CWLWarMember`: `tag`, `name`, `townHallLevel`, `mapPosition`

### Locations + Rankings
- `Location`: `id`, `name`, `isCountry`, `countryCode`
- `ClanRanking`: `tag`, `name`, `rank`, `previousRank`, `clanLevel`, `members`, `points`, `badgeUrls`
- `PlayerRanking`: `tag`, `name`, `rank`, `previousRank`, `expLevel`, `trophies`, `clan`
- `CapitalRanking`: `tag`, `name`, `rank`, `previousRank`, `clanLevel`, `points`, `badgeUrls`

### Leagues + Seasons
- `League`: `id`, `name`, `iconUrls`
- `LeagueSeason`: `id`
- `LeagueSeasonRank`: `tag`, `name`, `rank`, `previousRank`, `trophies`, `clan`

### Labels / GoldPass
- `ClanLabel`: `id`, `name`, `iconUrls`
- `GoldPassSeason`: `startTime`, `endTime`

## Нейминг методов (единый стиль)
- `get_*` для чтения; `*_page` для моделей с `items + paging`.
- Теги нормализуются через `normalize_tag()`.
- Пагинация через `paginate(limit, after)`.

