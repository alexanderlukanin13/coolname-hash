from hashlib import md5

from coolname.impl import _default

# Use fields and methods of default generator directly
_lst = _default._lists[None]
assert _default._ensure_unique is True  # always true for default generator, so we don't check it in function
assert _default._check_prefix == 4  # optimization
assert _default._max_slug_length == 50  # optimization
del _default


def pseudohash_tuple_v1(arg):
    """
    Similar to generate(), but returns deterministic result
    for the given argument (int, str or bytes).
    """
    # NOTE: hash will be the same for 123, '123' and b'123' - this is intentional
    if isinstance(arg, str):
        arg = arg.encode('utf8')
    elif isinstance(arg, int):
        arg = str(arg).encode('utf8')
    elif not isinstance(arg, bytes):
        raise ValueError('Unexpected type (must be int, str or bytes): {!r}'.format(arg))
    i = int.from_bytes(md5(arg).digest()[:8], byteorder='little')
    # Following is mostly copypaste from generate(), with minor changes and optimizations
    lst = _lst
    while True:
        i %= lst.length
        result = lst[i]
        # 1. Check that there are no duplicates or duplicate prefixes
        # 2. Check max slug length
        n = len(result)
        if len(set(x[:4] for x in result)) != n or sum(len(x) for x in result) + n - 1 > 50:
            i += 1
            continue
        return result


def pseudohash_slug_v1(arg):
    """
    Similar to generate_slug(), but returns deterministic result
    for the given argument (int, str or bytes).
    """
    return '-'.join(pseudohash_tuple_v1(arg))
