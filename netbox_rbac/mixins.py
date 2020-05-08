import collections
import re

from django.contrib.auth import mixins
from django.core.exceptions import PermissionDenied


class PermissionRequiredMixin(mixins.PermissionRequiredMixin):
    def get_permission_objects(self):
        # Single object view.
        if hasattr(self, "get_object") and callable(self.get_object):
            return [self.get_object(self.kwargs)]

        # Multiple objects view.
        pks = [int(pk) for pk in self.request.POST.getlist("pk")]

        if pks and hasattr(self, "queryset"):
            return self.queryset.model.objects.filter(pk__in=pks).iterator()

        return [None]

    def has_permission(self):
        objects = self.get_permission_objects()
        permissions = self.get_permission_required()

        denied = collections.defaultdict(list)

        for obj in objects:
            for perm in permissions:
                if self.request.user.has_perms([perm], obj):
                    continue

                # Extract the operation from the permission:
                #   <app>.<operation>_<class>
                match = re.match("^\w+\.([^_]+)", perm)

                # If the object is uninitialized, display something useful.
                if not str(obj):
                    obj = obj._meta.verbose_name_plural

                denied[match.group(1)].append(str(obj))

        if not denied:
            return True

        # Display a more informative exception.
        raise PermissionDenied(
            ", ".join(["%s %s" % (op, ", ".join(obj)) for op, obj in denied.items()])
        )
