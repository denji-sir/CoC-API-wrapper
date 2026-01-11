import pytest

from coc_api_wrapper.utils import normalize_tag, paginate


def test_normalize_tag_variants() -> None:
    assert normalize_tag("#abc") == "%23ABC"
    assert normalize_tag("abc") == "%23ABC"
    assert normalize_tag("%23abc") == "%23ABC"


def test_normalize_tag_empty_raises() -> None:
    with pytest.raises(ValueError):
        normalize_tag("   ")


def test_paginate_params() -> None:
    assert paginate(limit=10, after="cursor") == {"limit": 10, "after": "cursor"}

