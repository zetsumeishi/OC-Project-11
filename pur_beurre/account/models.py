from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import AccountManager
from product.models import Product


class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    favorites = models.ManyToManyField(Product)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
