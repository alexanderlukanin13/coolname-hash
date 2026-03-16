import re
from random import Random

import pytest

from coolname_hash import pseudohash_slug, _md5  # noqa

from src.coolname_hash import replace_random, generate_slug


def test_md5():
    """Ensure consistency of MD5 between Python releases. Just in case."""
    assert _md5(b'abc').digest() == b'\x90\x01P\x98<\xd2O\xb0\xd6\x96?}(\xe1\x7fr'

def test_pseudohash_slug():
    assert pseudohash_slug('abc') == 'humongous-gentle-jackal-from-avalon'


def test_int_str_bytes_same():
    assert pseudohash_slug('123456') == pseudohash_slug(b'123456')
    assert pseudohash_slug('123456') == pseudohash_slug(123456)
    assert pseudohash_slug('-123456') == pseudohash_slug(b'-123456')
    assert pseudohash_slug('-123456') == pseudohash_slug(-123456)
    assert pseudohash_slug('') == pseudohash_slug(b'')


def test_unsupported_types():
    with pytest.raises(TypeError, match=re.escape('Unexpected type "NoneType" (must be int, str or bytes): None')):
        pseudohash_slug(None)
    with pytest.raises(TypeError, match=re.escape('Unexpected type "bool" (must be int, str or bytes): True')):
        pseudohash_slug(True)
    with pytest.raises(TypeError, match=re.escape('Unexpected type "tuple" (must be int, str or bytes): ()')):
        pseudohash_slug(tuple())
    with pytest.raises(TypeError, match=re.escape('Unexpected type "list" (must be int, str or bytes): []')):
        pseudohash_slug(list())


def test_coverage():
    """Cover retries - at least one must happen"""
    slugs = set(pseudohash_slug(i) for i in range(1000))
    assert len(slugs) == 1000  # all must be unique, statistically


def test_coverage_replace_random():
    """There is a separate implementation of replace_random, so we need to cover it."""
    rand = Random()
    replace_random(rand)
    rand.seed(0)
    assert generate_slug() == 'liberal-adamant-auk-of-fascination'
