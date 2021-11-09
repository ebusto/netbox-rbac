import collections

from . import ldap, mock


Account = collections.namedtuple("Account", ["email", "first_name", "last_name"])


def load(config):
    if "LDAP" in config:
        return ldap.Driver(config["LDAP"])

    if "MOCK" in config:
        return mock.Driver(config["MOCK"])

    raise Exception("no auth driver configured")
