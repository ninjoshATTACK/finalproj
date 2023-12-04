from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birthday = models.DateField(blank=False)
    profile_pic = models.ImageField(blank=True)
    fname = models.CharField(blank=False, max_length=25)