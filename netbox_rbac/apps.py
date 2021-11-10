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
        import dcim.views
        import netbox.views

        from . import mixins

        include = {
            dcim.views.BulkDisconnectView:         mixins.BulkCheckView,
            netbox.views.generic.BulkDeleteView:   mixins.BulkCheckView,
            netbox.views.generic.BulkEditView:     mixins.BulkCheckView,
            netbox.views.generic.BulkRenameView:   mixins.BulkCheckView,
            netbox.views.generic.ObjectDeleteView: mixins.ObjectCheckView,
            netbox.views.generic.ObjectEditView:   mixins.ObjectCheckView,
        }

        # Core applications.
        apps = ["circuits", "dcim", "extras", "ipam", "tenancy", "virtualization"]
        conf = django.conf.settings.RBAC

        # Custom applications? Patch those too.
        if "APPS" in conf:
            apps += conf["APPS"]

        # For each view in each app, include the appropriate RBAC check.
        for app in apps:
            module = importlib.import_module("%s.views" % app)

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ != module.__name__:
                    continue

                bases = list(obj.__bases__)

                for i, base in enumerate(bases):
                    view = include.get(base)

                    if view:
                        bases.insert(i, view)
                        break

                obj.__bases__ = tuple(bases)
