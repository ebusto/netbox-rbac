from django.urls import path

from . import views


app_name = "rbac"

urlpatterns = [
    path("roles/", views.Roles.as_view(), name="roles"),
]
