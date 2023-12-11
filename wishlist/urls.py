from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from . import views, forms

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    path("password_reset/", auth_views.PasswordResetView.as_view(form_class=forms.MyPasswordResetForm), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path("add_friend/<int:user_id>", views.add_friend, name="add-friend"),
    path("send_friend_request/<int:user_id>", 
        views.send_friend_request, name="send-friend-request"),
    path("accept_friend_request/<int:request_id>",
        views.accept_friend_request, name="send-friend-request"),
    path("search_for_friend", views.search_for_friend, name="search-for-friend"),

    path("", views.index, name="index"),
    path("create_profile", views.create_profile, name="create-profile"),
    path("edit_profile", views.edit_profile, name="edit-profile"),
    path("my_wishlist", views.my_wishlist, name="my-wishlist"),
    path("create_wishlist", views.create_wishlist, name="create-wishlist"),
    path("edit_wishlist", views.edit_wishlist, name="edit-wishlist"),
    path("contact_us", views.contact_us, name="contact-us"),

    path("secret_santa", views.secret_santa, name="secret-santa"),
]