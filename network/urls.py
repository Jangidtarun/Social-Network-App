
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('newpost', views.newpost, name='newpost'),
    path('like/<int:post_id>', views.like, name='like'),
    path('<int:user_id>', views.viewuser, name='viewuser'),
    path('follow', views.follow, name='follow'),
    path('unfollow', views.unfollow, name='unfollow'),
    path('following', views.following, name='following'),
    path('saveeditpost/<int:post_id>', views.saveeditpost, name='saveeditpost')
]
