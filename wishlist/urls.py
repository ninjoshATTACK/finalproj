from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatters = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]