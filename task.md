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
- [ ] Добавить модели для WarLog, CWL LeagueGroup, CWL War, Locations/Rankings,
      Leagues/Seasons, Labels, GoldPass.
- [ ] Выделить общие подмодели (Season, Ranking, League, Label, WarMember).
- [ ] Обеспечить совместимость (extra="ignore" и корректные alias).

## Блок 3 — Методы клиента (sync/async)
- [ ] Добавить методы CoCClient под top-15 эндпоинтов.
- [ ] Добавить методы AsyncCoCClient под top-15 эндпоинтов.
- [ ] Проверить normalize_tag + paginate там, где нужно.

## Блок 4 — Bot i18n (RU/EN)
- [ ] Реализовать локализацию сообщений ошибок.
- [ ] Добавить резолвер локали: `BOT_LOCALE` (fallback `ru`).
- [ ] `format_bot_error(..., locale=...)` должен переопределять дефолт.
- [ ] Тесты на RU/EN + override.

## Блок 5 — Примеры и README
- [ ] Обновить README: список всех методов, примеры локалей.
- [ ] Обновить примеры (sync/async) с локалями.

## Блок 6 — Тесты по новым эндпоинтам
- [ ] Тесты на URL/params для новых методов (MockTransport).
- [ ] Тесты на парсинг моделей (минимальные JSON).
- [ ] Проверка edge cases (429, 404, 5xx).

## Блок 7 — Подготовка adapters (без реализации)
- [ ] Создать `coc_api_wrapper/adapters/` с заглушками.
- [ ] Добавить extras в `pyproject.toml` для `discord.py` и `aiogram`.
- [ ] Док-заметка: как подключать adapters.

## Блок 8 — Финальный прогон
- [ ] `ruff format .`
- [ ] `ruff check .`
- [ ] `pytest`
