# coc-api-wrapper

Удобный типизированный клиент к официальному Clash of Clans API, заточенный под ботов: вместо “сырого JSON” — Pydantic v2 модели, единые исключения и bot-friendly хелперы.

## Установка

```bash
python -m pip install -e ".[dev]"
```

## Быстрый старт (sync)

```python
from coc_api_wrapper import CoCClient

client = CoCClient(token="YOUR_TOKEN")
clan = client.get_clan("#ABC123")
print(clan.name, clan.members)
```

## Быстрый старт (async)

```python
import asyncio
from coc_api_wrapper import AsyncCoCClient


async def main() -> None:
    async with AsyncCoCClient(token="YOUR_TOKEN") as client:
        player = await client.get_player("#PLAYER")
        print(player.name, player.town_hall_level)


asyncio.run(main())
```

## Методы (0.1.0)

### Кланы и игроки
- `get_clan(tag)`
- `get_clan_members(tag, limit=None, after=None)`
- `get_player(tag)`
- `get_clan_warlog(tag, limit=None, after=None)`
- `get_current_war(clan_tag)`
- `get_capital_raids(clan_tag, limit=None, after=None)`

### CWL
- `get_cwl_group(clan_tag)`
- `get_cwl_leagues(limit=None, after=None)`
- `get_cwl_war(war_tag)`

### Локации и рейтинги
- `get_locations(limit=None, after=None)`
- `get_location_clan_rankings(location_id, limit=None, after=None)`
- `get_location_player_rankings(location_id, limit=None, after=None)`
- `get_location_capital_rankings(location_id, limit=None, after=None)`

### Лиги и сезоны
- `get_leagues(limit=None, after=None)`
- `get_league_seasons(league_id, limit=None, after=None)`
- `get_league_season(league_id, season_id, limit=None, after=None)`

### Labels / GoldPass
- `get_clan_labels(limit=None, after=None)`
- `get_current_goldpass()`

## Пагинация

Методы со списками принимают `limit` и `after` и возвращают `...Page`, у которых есть `page.after` (курсор следующей страницы).

## Нормализация тегов

Везде можно передавать `#ABC` / `ABC` / `%23ABC` — внутри используется `normalize_tag()`, который приводит к `%23ABC`.

## Ошибки

- `Unauthorized` (401/403)
- `NotFound` (404)
- `RateLimited(retry_after=...)` (429)
- `ServerError` (5xx)
- `APIError` (прочее)

## Для ботов: “без падений” в хендлере

Если удобнее возвращать результат/ошибку (а не ловить исключения в каждом хендлере), используйте `safe_await()`/`safe_call()` и `format_bot_error()`.

Если хотите **авто-повтор на 429**, используйте `safe_await_with_retry()`/`safe_call_with_retry()` — они подождут `Retry-After` (по умолчанию до 15s) и повторят запрос.

Локаль сообщений берется из `BOT_LOCALE` (fallback `ru`, поддерживаются `ru`/`en`, а также `ru-RU`/`en-US`). Можно переопределить на уровне конкретного ответа:

```python
format_bot_error(error, locale="en")
```

```python
from coc_api_wrapper import AsyncCoCClient, format_bot_error, safe_await_with_retry


async def handle_player(tag: str) -> str:
    async with AsyncCoCClient(token="YOUR_TOKEN") as client:
        result = await safe_await_with_retry(lambda: client.get_player(tag), max_retries=1)
        if not result.ok:
            return format_bot_error(result.error, locale="ru")
        return f"{result.value.name} TH={result.value.town_hall_level}"
```

## Retry/backoff + кэш

- Retry + backoff: автоматом на 429 и 5xx (настраивается через `max_retries`, `backoff_base`, `backoff_max`).
- In-memory TTL cache для GET: `cache_enabled=True/False`, `cache_ttl=...`.

## Debug-лог без токена

Включите `logging` для логгера `coc_api_wrapper` (заголовок `Authorization` автоматически редактируется).

## Adapters (planned)

Заготовлены модули под `discord.py` и `aiogram` (без реализации в v0.1.0).

```bash
python -m pip install -e ".[discord]"
python -m pip install -e ".[aiogram]"
```
