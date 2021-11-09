import django.apps
import django.conf
import importlib
import inspect


class AppConfig(django.apps.AppConfig):
    name = "netbox_rbac"

    def ready(self):
        # Patch the restricted queryset manager to remove view based restrictions.
        import utilities.querysets

        setattr(utilities.querysets.RestrictedQuerySet, "restrict", lambda qs, *args: qs)

        # Patch views.
        from .mixins import (
            BulkDeleteView,
            BulkEditView,
            BulkRenameView,
            ObjectDeleteView,
            ObjectEditView,
        )

        replace = {
            "BulkDeleteView":   BulkDeleteView,
            "BulkEditView":     BulkEditView,
            "BulkRenameView":   BulkRenameView,
            "ObjectDeleteView": ObjectDeleteView,
            "ObjectEditView":   ObjectEditView,
        }

        # Core applications.
        apps = ["circuits", "dcim", "extras", "ipam", "tenancy", "virtualization"]
        conf = django.conf.settings.RBAC

        # Custom applications? Patch those too.
        if "APPS" in conf:
            apps += conf["APPS"]

        # For each view in each app, replace various generic view classes.
        for app in apps:
            module = importlib.import_module("%s.views" % app)

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == module.__name__:
                    bases = list(obj.__bases__)

                    for i, base in enumerate(bases):
                        for name, view in replace.items():
                            if name == base.__name__:
                                bases[i] = view

                    obj.__bases__ = tuple(bases)
