import functools
import threading

from django.core.exceptions import PermissionDenied
from django.db.models.signals import m2m_changed, pre_save

# Ignore changes related to authentication.
ignore_modules = [
    "django.contrib.auth.models",
    "django.contrib.sessions.models",
    "netbox_rbac.models",
    "users.models",
]

# Track the current request so rules can evaluate request attributes.
requests = {}


def request():
    return requests.get(threading.current_thread())


class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        handler = functools.partial(self.has_perm, request)
        signals = (m2m_changed, pre_save)

        requests[threading.current_thread()] = request

        for signal in signals:
            signal.connect(handler)

        response = self.get_response(request)

        for signal in signals:
            signal.disconnect(handler)

        del requests[threading.current_thread()]

        return response

    def has_perm(self, request, instance, **kwargs):
        if instance.__module__ in ignore_modules:
            return

        # Determining the correct permission is surprisingly tricky.
        #
        # Operations performed via the REST API follow the typical REST method
        # convention, so we borrow the mapping from the Django REST framework.
        #
        # Operations performed via the web UI are less consistent, and mostly
        # use the POST method, so we have to see if the object already has a
        # primary key in order to distinguish between 'add' and 'change'.
        method_operation = {
            "DELETE": "delete",
            "GET": "view",
            "HEAD": "view",
            "PATCH": "change",
            "POST": "add",
            "PUT": "change",
        }

        oper = "change" if instance.pk else method_operation[request.method]

        perm = "%s.%s_%s" % (instance._meta.app_label, oper, instance._meta.model_name,)

        if not request.user.has_perms([perm], instance):
            raise PermissionDenied("%s %s" % (oper, instance))
