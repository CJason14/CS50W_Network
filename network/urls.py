from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("posts/<str:post>", views.posts, name="posts"),
    path("likes/<int:id>", views.likes, name="liked"),
    path("likes/all/<int:id>", views.alllikes, name="likes"),
    path("following", views.following, name="following"),
    path("user/<str:id>", views.getuser, name="user"),
    path("newpost", views.newpost, name="newpost"),
    path("getuserposts/<str:id>", views.getuserposts, name="getuserposts"),
    path("follow", views.follow, name="follow")
]
