import os

from coc_api_wrapper import CoCClient, format_bot_error, safe_call_with_retry


def main() -> None:
    token = os.environ["COC_API_TOKEN"]
    clan_tag = os.environ.get("COC_CLAN_TAG", "#2PP")
    locale = os.environ.get("BOT_LOCALE")

    client = CoCClient(token=token, cache_enabled=True, cache_ttl=30.0)
    clan_result = safe_call_with_retry(lambda: client.get_clan(clan_tag), max_retries=1)
    if not clan_result.ok:
        print(format_bot_error(clan_result.error, locale=locale))
        return
    members_result = safe_call_with_retry(
        lambda: client.get_clan_members(clan_tag, limit=5),
        max_retries=1,
    )
    if not members_result.ok:
        print(format_bot_error(members_result.error, locale=locale))
        return

    clan = clan_result.value
    members = members_result.value
    assert clan is not None
    assert members is not None

    print(f"{clan.name} ({clan.tag}) level={clan.clan_level} members={clan.members}")
    for member in members.items:
        print(f"- {member.name} {member.tag} role={member.role} trophies={member.trophies}")


if __name__ == "__main__":
    main()
