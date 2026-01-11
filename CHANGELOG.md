# Changelog

## v0.1.0 — 2026-01-11

### Highlights
- Первый публичный релиз типизированного CoC API клиента (sync/async) на httpx + Pydantic v2.
- Bot-first хелперы: безопасные вызовы, авто-retry на 429, локализация RU/EN.
- Базовая инфраструктура: тесты, CI, примеры, карта эндпоинтов.

### Features
- 15 ключевых эндпоинтов CoC API: кланы/игроки, warlog, CWL, лиги/сезоны, локации и рейтинги, labels, gold pass.
- Пагинация `limit/after` с курсором `page.after`.
- TTL-кэш GET, retry/backoff на 429 и 5xx, нормализация тегов.
- Унифицированные исключения и редактирование токена в логах.
- Заготовки адаптеров для discord.py и aiogram (без реализации).

### Performance
- In-memory TTL кэш для GET-ответов.

### Security
- Редакция `Authorization` в debug-логах.

### Dependencies
- httpx, pydantic (core).
- pytest, pytest-asyncio, ruff (dev).
- discord.py/aiogram (optional extras).

### Operations
- CI: ruff + pytest.

### Known issues
- Неполное покрытие всех эндпоинтов CoC API.
- Модели содержат минимальные поля (лишние игнорируются).
- Адаптеры для ботов пока заглушки.
