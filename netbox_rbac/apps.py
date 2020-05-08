import django.apps
import django.conf
import importlib
import inspect

# Core applications.
apps = [
    "circuits",
    "dcim",
    "extras",
    "ipam",
    "tenancy",
    "virtualization",
]

config = django.conf.settings.RBAC

# Custom applications? Patch those too.
if "APPS" in config:
    apps += config["APPS"]


class AppConfig(django.apps.AppConfig):
    name = "netbox_rbac"

    def ready(self):
        from .mixins import PermissionRequiredMixin

        # For each view in each app, replace PermissionRequiredMixin with ours.
        for app in apps:
            module = importlib.import_module("%s.views" % app)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == module.__name__:
                    bases = list(obj.__bases__)

                    for i, base in enumerate(bases):
                        if base.__name__ == "PermissionRequiredMixin":
                            bases[i] = PermissionRequiredMixin

                    obj.__bases__ = tuple(bases)

        # Patch views which don't otherwise have an easy way to get objects.
        import dcim.models
        import dcim.views

        patch = [
            (dcim.views.VirtualChassisAddMemberView, dcim.models.VirtualChassis),
            (dcim.views.VirtualChassisEditView, dcim.models.VirtualChassis),
            (dcim.views.VirtualChassisRemoveMemberView, dcim.models.VirtualChassis),
        ]

        for view, model in patch:
            setattr(
                view,
                "get_object",
                lambda self, kwargs: model.objects.get(pk=kwargs["pk"]),
            )
