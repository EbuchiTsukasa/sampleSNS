from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("home/", views.Home.as_view, name='home'),
    path("mypost/", views.MyPost.as_view(), name='mypost'),
    path("follow-list/", views.FollowList.as_view(), name='follow-list'),
]