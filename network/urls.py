
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all_posts/<str:user>", views.all_posts, name="all_posts"),

    #API
    path("follow_or_unfollow/<str:user>", views.follow_or_unfollow, name="follow_or_unfollow"),
    path("is_followed", views.is_followed, name="is_followed")
    
]
