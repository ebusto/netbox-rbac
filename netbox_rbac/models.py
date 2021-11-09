from django.contrib.auth.models     import User
from django.contrib.postgres.fields import ArrayField

from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    roles = ArrayField(models.CharField(max_length=255), blank=True, default=list,)

    class Meta:
        managed = True
