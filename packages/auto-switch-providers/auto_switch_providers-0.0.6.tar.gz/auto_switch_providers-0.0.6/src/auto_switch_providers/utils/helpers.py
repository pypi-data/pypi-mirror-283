import base64
import functools
from json import dumps


def nested_dict_get(dictionary, dotted_key):
    keys = dotted_key.split(".")
    return functools.reduce(
        lambda d, key: (
            d[int(key)] if isinstance(d, list) else d.get(key) if d else None
        ),
        keys,
        dictionary,
    )


def merge_child(raw_dict: dict):
    return {k: [d.get(k) for d in raw_dict] for k in set().union(*raw_dict)}


def base64encode(data):
    return base64.b64encode(dumps(data).encode("utf-8")).decode("utf-8")


def base64decode(string: str):
    return base64.b64decode(string)
