from random import Random

import coolname
from coolname.impl import _md5

from ._version import __version__, __version_tuple__  # noqa


__all__ = ['RandomGenerator', 'generate', 'generate_slug', 'get_combinations_count', 'pseudohash', 'pseudohash_slug']


try:
    int.from_bytes(b'\xFF\xFF\xFF\xFF')
    _bytes_to_int = int.from_bytes  # noqa
except TypeError:  # pragma: no cover
    import functools
    _bytes_to_int = functools.partial(int.from_bytes, byteorder='big')  # noqa


def _poor_mans_rng(seed: int, length: int):
    # Dumb-but-cheap replacement for RNG to retry after bad combinations
    # (repeated prefixes, too long, etc.)
    max_pow = len(str(abs(length)))
    cur_pow = 0
    i = seed
    while True:
        i = i + 10**cur_pow
        yield i % length
        cur_pow = (cur_pow + 1) % max_pow


class RandomGenerator(coolname.RandomGenerator):
    """Drop-in replacement for coolname.RandomGenerator"""

    def pseudohash(self, obj: int | str | bytes, pattern: str | int | None = None) -> list[str]:
        """
        Similar to generate(), but returns deterministic result for a hashable object.

        WARNING: collisions are possible - uniqueness not guaranteed!
        """
        lst = self._lists[pattern]
        # NOTE: hash will be the same for 123, '123' and b'123' - this is intentional
        if isinstance(obj, str):
            obj = obj.encode('utf8')
        elif isinstance(obj, int) and not isinstance(obj, bool):
            obj = str(obj).encode('utf8')
        elif not isinstance(obj, bytes):
            raise TypeError(f'Unexpected type "{type(obj).__qualname__}" (must be int, str or bytes): {obj!r}')
        i = _bytes_to_int(_md5(obj).digest()[:8]) % lst.length  # type: ignore
        while True:
            result = lst[i]
            # 1. Check that there are no duplicates
            # 2. Check that there are no duplicate prefixes
            # 3. Check max slug length
            n = len(result)
            if (self._ensure_unique and len(set(result)) != n or
                    self._check_prefix and len(set(x[:self._check_prefix] for x in result)) != n or
                    self._max_slug_length and sum(len(x) for x in result) + n - 1 > self._max_slug_length):
                try:
                    i = next(p)  # type: ignore
                except NameError:
                    p = _poor_mans_rng(i, lst.length)
                    i = next(p)
                continue
            # Most of the time it returns at first attempt, without repeating the loop.
            # Note about typing: technically its List[str] | str, but we know it's always List[str] at this point.
            return result  # type: ignore

    def pseudohash_slug(self, obj: int | str | bytes, pattern: str | int | None = None) -> str:
        """
        Similar to generate_slug(), but returns deterministic result for a hashable object.

        WARNING: collisions are possible - uniqueness not guaranteed!
        """
        return '-'.join(self.pseudohash(obj, pattern))


class _DefaultRandomGenerator(RandomGenerator):

    def __init__(self, default: coolname.RandomGenerator):  # noqa
        self.random = default.random
        self._lists = default._lists
        self._ensure_unique = default._ensure_unique
        self._check_prefix = default._check_prefix
        self._max_slug_length = default._max_slug_length


# Default generator is a global object
_default: RandomGenerator = _DefaultRandomGenerator(coolname.impl._default)

# Global functions are actually methods of the default generator.
# (most users don't care about creating generator instances)
generate = _default.generate
generate_slug = _default.generate_slug
get_combinations_count = _default.get_combinations_count
pseudohash = _default.pseudohash
pseudohash_slug = _default.pseudohash_slug


def replace_random(rand: Random | None = None) -> None:
    """Replaces random number generator for the default RandomGenerator instance."""
    _default.random = rand
