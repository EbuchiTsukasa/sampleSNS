from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("home/<int:pk>", views.Home.as_view, name='home'),
    path("mypost/<int:pk>", views.MyPost.as_view(), name='mypost'),
    path("other_user_post_list/<int:pk>", views.OtherUserPostList.as_view(), name='other_user_post_list'),
    path("like_delete/<int:pk>", views.LikeDelete.as_view(), name='like_delete'),
    path("like_create/<int:pk>", views.LikeCreate.as_view(), name='like_create'),
]