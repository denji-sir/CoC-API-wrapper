from coc_api_wrapper.cache import TTLCache


def test_ttl_cache_expires() -> None:
    now = [0.0]

    def time_fn() -> float:
        return now[0]

    cache: TTLCache[dict[str, int]] = TTLCache(enabled=True, default_ttl=1.0, time_fn=time_fn)
    cache.set("k", {"a": 1})
    assert cache.get("k") == {"a": 1}

    now[0] = 2.0
    assert cache.get("k") is None
