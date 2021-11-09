import deepmerge
import functools
import importlib
import logging
import yaml

from inspect import getmembers, isfunction
from urllib  import parse, request
from wcmatch import fnmatch

from . import macros, middleware


try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

log = logging.getLogger("netbox_rbac")

# Collect all public functions from macros.
functions = [
    (name, fn)
    for name, fn in getmembers(macros, isfunction)
    if not name.startswith("_")
]

# In order to guard against external dependencies, such as Gitlab, being
# unavailable, store the last configuration.
config = None


def load(paths):
    global config

    errors = []

    for path in paths:
        try:
            path = parse.urlparse(path, scheme="file")
            data = request.urlopen(path.geturl())

            config = Rule(yaml.load(data, Loader=Loader))

            return config

        except Exception as err:
            errors.append("%s: %s" % (path.geturl(), err))

    log.warn("load: no valid rules found: %s", errors)

    # Unable to load a new config, so return the current one.
    return config


class Rule:
    def __init__(self, config):
        self.roles = {}

        # Although YAML provides a mechanism for referencing one object from
        # another, it doesn't support deep merging, so we handle that manually.
        for name, role in config.items():
            for base in role.get("base", []):
                deepmerge.always_merger.merge(role, config[base])

            # Ignore template roles.
            if "groups" in role:
                self.roles[name] = Role(name, **role)

    # Given the user's roles, the requested permission, and the object, returns
    # whether or not the operation is allowed.
    def has_perm(self, roles, perm, obj):
        for role in roles:
            role = self.roles.get(role)

            # Permission is granted when:
            #  * The role is valid (defined in the configuration).
            #  * The requested permission is granted by the role.
            #  * The rule evaluates to True on the object.
            if role and role.has_perm(perm) and role.eval(obj):
                return True

        return False


class Role:
    def __init__(self, name, **kwargs):
        self.name    = name
        self.context = kwargs.get("context", {})
        self.groups  = kwargs.get("groups",  [])
        self.imports = kwargs.get("imports", [])
        self.perms   = kwargs.get("perms",   [])
        self.rule    = kwargs.get("rule")

        if self.rule:
            self.code = compile(self.rule, "<string>", "eval")
        else:
            self.code = None

    # Returns the result of evaluating the rule on the object, if both are
    # defined. Returns True otherwise.
    def eval(self, obj):
        if self.code and obj:
            context = {**self.context, "obj": obj}

            for name in self.imports:
                context[name] = importlib.import_module(name)

            for name, fn in functions:
                context[name] = functools.partial(fn, obj)

            context.update({
                "fnmatch": fnmatch.fnmatch,
                "request": middleware.request(),
            })

            return eval(self.code, context)

        return True

    # Returns whether or not this role provides the requested permission.
    def has_perm(self, perm):
        return fnmatch.fnmatch(perm, self.perms)
