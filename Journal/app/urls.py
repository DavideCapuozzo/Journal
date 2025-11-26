from django.urls import path
from . import views


urlpatterns = [
    path('', views.journal, name='journal'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("blogpost", views.blogpost_request, name="blogpost"),
    path("post", views.blogpost_request, name="post"),
    path("logout", views.custom_logout, name="logout"),
    path("search_post", views.search_post, name="search_post"),
    path("post_details/<int:id>", views.post_details, name="post_details"),
]