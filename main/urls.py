from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("home/", views.Home.as_view(), name='home'),
    path("mypost/", views.MyPost.as_view(), name='mypost'),
    path("other_user_post_list/", views.OtherUserPostList.as_view(), name='other_user_post_list'),
    path("like_delete/<int:pk>", views.LikeDelete.as_view(), name='like_delete'),
    path("like_create/<int:pk>", views.LikeCreate.as_view(), name='like_create'),
    path("follow/<int:pk>", views.Follow.as_view(), name='follow'),
    path("unfollow/<int:pk>", views.Unfollow.as_view(), name='unfollow')
]