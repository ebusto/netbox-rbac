import ldap

from .. import auth

# Required when using self-signed certificates.
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)


class Driver:
    def __init__(self, config):
        self.config = config

    def session(self):
        return Session(**self.config)


class Session:
    def __init__(self, domain, search, server):
        self.domain = domain
        self.search = search

        # Cache group membership to avoid repeated lookups.
        self.groups = {}

        # Connect, and ensure the connection is encrypted.
        self.client = ldap.initialize(server)
        self.client.start_tls_s()

    def authenticate(self, username, password):
        # Authenticate as the user.
        self.client.simple_bind_s(self.domain + "\\" + username, password)

        # Retrieve user attributes.
        result = self.lookup("user", username)

        if not result:
            raise Exception("search: no results")

        # Each result is a tuple: (distinguishedName, attributes)
        attrs = result[1]
        props = {
            "email":      "mail",
            "first_name": "givenName",
            "last_name":  "sn",
        }

        # Map from LDAP attributes to account properties.
        for prop, attr in props.items():
            props[prop] = ""

            if attr in attrs and attrs[attr]:
                props[prop] = attrs[attr][0].decode("utf8")

        return auth.Account(**props)

    def close(self):
        self.client.unbind_ext_s()

    def lookup(self, kind, *args):
        results = self.client.search_s(
            self.search[kind]["base"], ldap.SCOPE_SUBTREE,
            self.search[kind]["filter"] % tuple(args),
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
