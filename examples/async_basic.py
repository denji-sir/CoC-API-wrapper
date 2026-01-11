import asyncio
import os

from coc_api_wrapper import AsyncCoCClient, format_bot_error, safe_await_with_retry


async def main() -> None:
    token = os.environ["COC_API_TOKEN"]
    player_tag = os.environ.get("COC_PLAYER_TAG", "#2PP")
    locale = os.environ.get("BOT_LOCALE")

    async with AsyncCoCClient(token=token, cache_enabled=True, cache_ttl=30.0) as client:
        result = await safe_await_with_retry(lambda: client.get_player(player_tag), max_retries=1)
        if not result.ok:
            print(format_bot_error(result.error, locale=locale))
            return

        player = result.value
        assert player is not None
        print(
            f"{player.name} ({player.tag}) th={player.town_hall_level} trophies={player.trophies}"
        )


if __name__ == "__main__":
    asyncio.run(main())
