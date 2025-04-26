from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer')
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CHOICES[1][0])

    def __str__(self):
        return self.username