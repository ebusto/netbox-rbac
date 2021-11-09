import cachetools
import django.conf

from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

from . import auth, models, rule


# Django creates an instance of Backend for every permission check. Since
# loading rules is somewhat expensive, we memoize the configuration items, as
# well as flush periodically to ensure we're using the latest rules.
@cachetools.cached(cache=cachetools.TTLCache(maxsize=128, ttl=60))
def cached_config(key):
    config = django.conf.settings.RBAC

    if key == "auth":
        return auth.load(config["AUTH"])

    if key == "rule":
        return rule.load(config["RULE"])

    raise Exception("cached_config: unknown key: %s" % key)


class Backend:
    def __init__(self, **kwargs):
        self.auth = kwargs.get("auth", cached_config("auth"))
        self.rule = kwargs.get("rule", cached_config("rule"))

    def authenticate(self, request, username=None, password=None):
        sn = self.auth.session()

        try:
            account = sn.authenticate(username, password)
        except Exception:
            raise PermissionDenied

        # Credentials are valid. Ensure the user object exists.
        user, _ = User.objects.get_or_create(username=username)

        # Determine roles from group membership.
        roles = set()

        for name, role in self.rule.roles.items():
            if sn.member(username, role.groups):
                roles.add(name)

        user.email      = account.email
        user.first_name = account.first_name
        user.last_name  = account.last_name

        if "_is_denied" in roles:
            roles.clear()

        user.is_active    = "_is_active" in roles
        user.is_staff     = "_is_staff"  in roles
        user.is_superuser = "_is_super"  in roles

        user.save()

        profile, _ = models.Profile.objects.get_or_create(user=user)

        profile.roles = sorted(list(roles))
        profile.save()

        # Close the session.
        sn.close()

        return user

    def get_user(self, user_id):
        user = User.objects.get(pk=user_id)

        # Ensure each user has a profile.
        if user and not hasattr(user, "profile"):
            models.Profile.objects.create(user=user)

        return user

    def has_perm(self, user_obj, perm, obj=None):
        if hasattr(user_obj, "profile"):
            return self.rule.has_perm(user_obj.profile.roles, perm, obj)

        return False
