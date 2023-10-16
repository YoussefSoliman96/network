
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following/<str:username>", views.following, name="following"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like"),
    path("unlike/<int:post_id>", views.unlike, name="unlike"),
    path("delete_post/<int:post_id>", views.delete_post, name="delete"),
    path("comment/<int:post_id>", views.comment, name="comment"),
    path("delete_comment/<int:comment_id>", views.delete_comment, name="delete_comment"),

]
