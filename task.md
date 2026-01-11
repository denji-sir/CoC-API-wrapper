## Блок 0 — Базовый каркас (готово)
- [x] Core sync/async клиент, utils, cache, exceptions.
- [x] Pydantic v2 модели для MVP (Clan/Player/CurrentWar/RaidSeasons).
- [x] Bot helpers (safe_call/safe_await + retry-429 helpers).
- [x] Примеры, тесты, CI, README.

## Блок 1 — Карта эндпоинтов (top-15)
- [x] Зафиксировать итоговый список методов + пути (см. `endpoint_map.md`).
- [x] Определить минимальные поля для моделей (с вложенностями).
- [x] Сверить нейминг методов для API клиента.

## Блок 2 — Модели данных (Pydantic v2)
- [x] Добавить модели для WarLog, CWL LeagueGroup, CWL War, Locations/Rankings,
      Leagues/Seasons, Labels, GoldPass.
- [x] Выделить общие подмодели (Season, Ranking, League, Label, WarMember).
- [x] Обеспечить совместимость (extra="ignore" и корректные alias).

## Блок 3 — Методы клиента (sync/async)
- [x] Добавить методы CoCClient под top-15 эндпоинтов.
- [x] Добавить методы AsyncCoCClient под top-15 эндпоинтов.
- [x] Проверить normalize_tag + paginate там, где нужно.

## Блок 4 — Bot i18n (RU/EN)
- [x] Реализовать локализацию сообщений ошибок.
- [x] Добавить резолвер локали: `BOT_LOCALE` (fallback `ru`).
- [x] `format_bot_error(..., locale=...)` должен переопределять дефолт.
- [x] Тесты на RU/EN + override.

## Блок 5 — Примеры и README
- [x] Обновить README: список всех методов, примеры локалей.
- [x] Обновить примеры (sync/async) с локалями.

## Блок 6 — Тесты по новым эндпоинтам
- [x] Тесты на URL/params для новых методов (MockTransport).
- [x] Тесты на парсинг моделей (минимальные JSON).
- [x] Проверка edge cases (429, 404, 5xx).

## Блок 7 — Подготовка adapters (без реализации)
- [x] Создать `coc_api_wrapper/adapters/` с заглушками.
- [x] Добавить extras в `pyproject.toml` для `discord.py` и `aiogram`.
- [x] Док-заметка: как подключать adapters.

## Блок 8 — Финальный прогон
- [x] `ruff format .`
- [x] `ruff check .`
- [x] `pytest`
