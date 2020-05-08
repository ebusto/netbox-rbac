from wcmatch.fnmatch import fnmatch


def get(obj, path):
    for attr in path.split("."):
        if not hasattr(obj, attr):
            return None

        obj = getattr(obj, attr)

    return obj


def match(obj, *args):
    *paths, values = args

    return _walk_match(obj, paths, values, False)


def match_or_none(obj, *args):
    *paths, values = args

    return _walk_match(obj, paths, values, True)


def _walk_match(obj, paths, values, default):
    for path in paths:
        value = get(obj, path)

        if value is not None:
            return fnmatch(value, values)

    return default
