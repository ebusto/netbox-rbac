import ldap
import logging

from .. import auth


# TODO(shakefu): Move this into the plugin configuration
USE_TLS = False


# TODO(shakefu): Move this to a logging module for better DRY
log = logging.getLogger("netbox_rbac")


class Driver:
    def __init__(self, config):
        self.config = config
        # TODO(shakefu): Remove this, it's insanely noisy
        # log.debug(f"New Driver config:\n{self.config}")

    def session(self):
        return Session(**self.config)


class Session:
    def __init__(self, domain, search, server):
        log.debug(f"New Session for {domain}")

        self.domain = domain
        self.search = search

        # Cache group membership to avoid repeated lookups.
        self.groups = {}

        # TBD(shakefu): Move this client out of the Session? Is `ldap`
        # threadsafe?

        log.debug(f"Connecting to {server}")

        # Connect, and ensure the connection is encrypted.
        self.client = ldap.initialize(server)

        # Required when using self-signed certificates.
        if USE_TLS:
            log.debug("Initializing TLS Session")
            self.client.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            self.client.start_tls_s()

    def authenticate(self, username, password):
        # Authenticate as the user.

        # XXX(shakefu): AD style login DN?
        # who = self.domain + "\\" + username

        # LDAP style login DN
        # domain = ','.join([f"DC={c}" for c in self.domain.split('.')])
        # who = f"CN={username},{domain}"

        # Everything looks like a Nail
        # who = f"CN={username},CN=Users,DC=example,DC=org"
        # who = f"{username}"
        who = f"{username}@{self.domain}"

        # TODO(shakefu): Remove password logging
        log.debug(f"Authenticating as '{who}' with '{password}'")

        # self.client.simple_bind_s(self.domain + "\\" + username, password)
        self.client.simple_bind_s(who, password)

        # Retrieve user attributes.
        result = self.lookup("user", username)

        log.debug(f"Lookup result: {result}")

        if not result:
            raise Exception("search: no results")

        # Each result is a tuple: (distinguishedName, attributes)
        attrs = result[1]
        props = {
            "email": "mail",
            "first_name": "givenName",
            "last_name": "sn",
        }

        # Map from LDAP attributes to account properties.
        for prop, attr in props.items():
            props[prop] = ""

            if attr in attrs and attrs[attr]:
                props[prop] = attrs[attr][0].decode("utf8")

        log.debug(f"Props: {props}")

        return auth.Account(**props)

    def close(self):
        self.client.unbind_ext_s()

    def lookup(self, kind, *args):
        base = self.search[kind]["base"]
        scope = ldap.SCOPE_SUBTREE
        search = self.search[kind]["filter"] % tuple(args)

        log.debug(f"base: {base} scope: {scope} search: {search}")

        results = self.client.search_s(
            base,
            scope,
            search,
        )

        return next(iter(results), None)

    def member(self, username, groups):
        for group in groups:
            # Populate the cache for this group, if necessary.
            if group not in self.groups:
                self.groups[group] = self.member_query(username, group)

            if self.groups[group]:
                return True

        return False

    def member_query(self, username, group):
        # Get the DN of the group.
        group = self.lookup("group", group)

        # Get membership.
        if group and self.lookup("member", username, group[0]):
            return True

        return False
