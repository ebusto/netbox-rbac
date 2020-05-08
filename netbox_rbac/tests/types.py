from collections import namedtuple

__all__ = [
    "Rack",
    "Site",
]

Rack = namedtuple("Rack", ["name", "site"])
Site = namedtuple("Site", ["name"])
