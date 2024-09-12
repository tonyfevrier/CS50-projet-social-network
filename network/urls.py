
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.register_post, name="register_post"),
    path("someposts/<str:whichposts>", views.view_some_posts, name="view_some_posts"),
    path("profile/<str:username>", views.view_profile, name="view_profile"),
]
