## Goal
- Закрыть MVP + top-N (15) эндпоинтов CoC API, с типизированными Pydantic v2 моделями и единым клиентом (sync/async).
- Сделать bot-first слой: безопасные хелперы + локализация RU/EN (по умолчанию из `BOT_LOCALE`, с override в `format_bot_error(..., locale=...)`).
- Подготовить основу для optional adapters под `discord.py` и `aiogram` (без внедрения в v0.1.0).

## Assumptions / constraints
- Python 3.11+, Pydantic v2, httpx, Ruff, Pytest.
- Без сетевых тестов: использовать `httpx.MockTransport`.
- Локаль по умолчанию — `ru`, берется из `BOT_LOCALE`.
- В v0.1.0 нет прямых интеграций с конкретными фреймворками, только core + helpers.

## Research (current state)
- Modules/subprojects involved:
  - `coc_api_wrapper/`
- Key files/paths:
  - `coc_api_wrapper/client.py`
  - `coc_api_wrapper/async_client.py`
  - `coc_api_wrapper/models.py`
  - `coc_api_wrapper/exceptions.py`
  - `coc_api_wrapper/bot.py`
  - `coc_api_wrapper/utils.py`
  - `coc_api_wrapper/cache.py`
  - `coc_api_wrapper/__init__.py`
  - `README.md`
  - `examples/`
  - `tests/`
  - `pyproject.toml`
  - `.github/workflows/ci.yml`
  - `coc_api_wrapper/AGENTS.md`
- Entrypoints (API/UI/CLI/Jobs):
  - `CoCClient`, `AsyncCoCClient`, bot helpers (`safe_*`, `format_bot_error`)
- Related configs/flags:
  - `BOT_LOCALE`
- Data models/storage touched:
  - Pydantic v2 модели в `coc_api_wrapper/models.py`
- Interfaces/contracts (APIs/events/IPC):
  - CoC REST API endpoints
- Existing patterns to follow:
  - единый `_request()` с retry/backoff, TTL cache, нормализация тега
  - `httpx.MockTransport` в тестах

## Analysis
### Options
1) Optional adapters как отдельные модули в этом пакете с extras (`[discord]`, `[aiogram]`).
2) Вынести adapters в отдельные пакеты (больше контроля версий, но сложнее поддержка).

### Decision
- Chosen: Option 1.
- Why: проще дистрибуция для пользователя и меньше фрагментации на ранней стадии.

### Risks / edge cases
- Изменения в CoC API могут ломать модели (нужно гибко игнорировать лишние поля).
- Rate-limit (429) и поведение retry/backoff должны быть предсказуемыми для ботов.
- Локализация сообщений должна покрывать все типы ошибок и корректно fallback-ить.
- Часть эндпоинтов имеет специфические поля/структуры (warlog, league seasons).

### Open questions
- Нет.

## Q&A results (captured after the session)
- Outcome/acceptance criteria:
  - Core: sync/async клиент + модели Pydantic v2 для MVP + top-15 эндпоинтов, единые ошибки, retry/backoff, кеш, пагинация.
  - Bot layer: safe_call/safe_await (+ авто-retry 429), локализация RU/EN с `BOT_LOCALE` и override в `format_bot_error`.
  - Продукт: README, примеры, tests, CI (ruff+pytest), py.typed, структура пакета.
- Scope boundaries:
  - v0.1.0: core + helpers, без конкретных bot-фреймворков.
  - Подготовить plan для adapters `discord.py` + `aiogram`.
- Constraints/non-goals:
  - Тесты без сети (MockTransport).
  - Локаль default `ru` из `BOT_LOCALE`.
- Known modules/paths/subprojects:
  - `coc_api_wrapper/`, `examples/`, `tests/`
- Decisions made in Q&A:
  - Core + helpers + optional adapters.
  - RU/EN локализация: default из `BOT_LOCALE`, override параметром в `format_bot_error`.
  - Top-N = 15 эндпоинтов:
    - `clans/{tag}/warlog`
    - `clans/{tag}/currentwar` (already in MVP)
    - `clans/{tag}/currentwar/leaguegroup`
    - `clans/{tag}/capitalraidseasons` (already in MVP)
    - `clanwarleagues/warleagues`
    - `clanwarleagues/wars/{id}`
    - `locations`
    - `locations/{id}/rankings/clans`
    - `locations/{id}/rankings/players`
    - `locations/{id}/rankings/capital`
    - `leagues`
    - `leagues/{id}/seasons`
    - `leagues/{id}/seasons/{seasonId}`
    - `labels/clans`
    - `goldpass/seasons/current`
- Remaining open questions (if any):
  - Нет.

## Implementation plan
1) Сформировать карту эндпоинтов и модели для MVP + top-15, определить минимальные поля и вложенности.
2) Расширить `CoCClient`/`AsyncCoCClient` методами под список эндпоинтов.
3) Расширить `models.py` (минимальные Pydantic v2 модели под новые ответы).
4) Добавить i18n слой для bot-ошибок:
   - `BOT_LOCALE` как дефолт (fallback `ru`).
   - `format_bot_error(..., locale=...)` с override.
5) Обновить/добавить примеры под bot-first использование (sync/async + локаль).
6) Тесты:
   - Валидация URL/params и paginated responses.
   - i18n ошибок (RU/EN + override).
   - Retry/429 поведение в bot helpers.
7) Обновить README:
   - Полный список методов и endpoints.
   - Пример с локалями и bot helper layer.
8) Подготовить структуру для adapters (без реализации в v0.1.0):
   - `coc_api_wrapper/adapters/discord.py`
   - `coc_api_wrapper/adapters/aiogram.py`
   - extras в `pyproject.toml`

## Tests to run
- `ruff format .`
- `ruff check .`
- `pytest`

