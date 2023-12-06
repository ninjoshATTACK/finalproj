from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birthday = models.DateField(blank=True, null=True)
    profile_pic = models.ImageField(blank=True)
    fname = models.CharField(blank=True, max_length=50)
    friends = models.ManyToManyField('User', blank=True)

class Friend_Request(models.Model):
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE
    )

class Wishlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    #Faves
    fav_color = models.CharField(max_length=64)
    fav_food = models.CharField(max_length=64)
    fav_drink = models.CharField(max_length=64)
    fav_candy = models.CharField(max_length=64)
    fav_animal = models.CharField(max_length=64)
    fav_media = models.CharField(max_length=64)
    fav_hobbie = models.CharField(max_length=64)
    fav_book = models.CharField(max_length=64)
    fav_music = models.CharField(max_length=64)
    additional = models.TextField(max_length=500)
