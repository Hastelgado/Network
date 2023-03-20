
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<str:userid>", views.profile, name="profile"),
    path("follow/<str:userid>", views.follow, name="follow"),
    path("unfollow/<str:userid>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("edit/<str:postid>", views.edit, name="edit"),
    path("like", views.like, name="like"),
    path("unlike", views.unlike, name="unlike"),
]
