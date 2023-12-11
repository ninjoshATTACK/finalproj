from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    friends = models.ManyToManyField('User', blank=True)
    wishlist_done = models.BooleanField(default=False)
    profile_done = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='images/profile_images')
    fname = models.CharField(blank=True, max_length=50)
    lname = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return f'{self.user.username}\'s profile'

class Friend_Request(models.Model):
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE
    )

class Wishlist(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    #Faves
    fav_color = models.CharField(max_length=64)
    fav_food = models.CharField(max_length=64)
    fav_drink = models.CharField(max_length=64)
    fav_candy = models.CharField(max_length=64)
    fav_animal = models.CharField(max_length=64)
    fav_media = models.CharField(max_length=64) #movie/tv/anime
    fav_hobby = models.CharField(max_length=64)
    fav_book = models.CharField(max_length=64)
    fav_game = models.CharField(max_length=64)
    fav_music = models.CharField(max_length=64) #artist
    
    gift_ideas = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.owner.username}\'s wishlist'
    
""" class AssignedSanta(models.Model):
    santa = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE
    )
    santee = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE
    )

class SecretSanta(models.Model):
    creator = models.OneToOneField(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField('User', blank=True)

    def assign_santas(self):
        p = self.participants.all()
        t = []

        for i in p:
            pass """