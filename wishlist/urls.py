from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("add_friend", views.add_friend, name="add-friend"),
    path("send_friend_request/<int:user_id>", 
        views.send_friend_request, name="send-friend-request"),
    path("accept_friend_request/<int:user_id>",
        views.accept_friend_request, name="send-friend-request"),

    path("", views.index, name="index"),
    path("edit_profile", views.edit_profile, name="edit-profile"),
    path("my_wishlist", views.my_wishlist, name="my-wishlist"),
    path("create_wishlist", views.create_wishlist, name="create-wishlist"),

    path("secret_santa", views.secret_santa, name="secret-santa"),
]