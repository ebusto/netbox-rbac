from django.shortcuts import render
from django.views.generic import View

from .backend import Backend


class Roles(View):
    def get(self, request):
        backend = Backend()
        context = {
            "rule": backend.rule,
            "user": request.user,
        }

        return render(request, "netbox_rbac/roles.html", context)
