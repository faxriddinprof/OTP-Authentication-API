from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    tg_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name