from django.contrib import admin
from .models import Profile, Friend_Request, Wishlist

# Register your models here.
admin.site.register(Profile)
admin.site.register(Friend_Request)
admin.site.register(Wishlist)