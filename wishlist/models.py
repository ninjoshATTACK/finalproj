from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    friends = models.ManyToManyField('User', blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='images/profile_images')
    fname = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

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
    fav_media = models.CharField(max_length=64) #movie/tv/anime
    fav_hobby = models.CharField(max_length=64)
    fav_book = models.CharField(max_length=64)
    fav_game = models.CharField(max_length=64)
    fav_music = models.CharField(max_length=64) #artist
    
    gift_ideas = models.TextField(max_length=500)
