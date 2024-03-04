from django.db.models.query import QuerySet
from .models import Post, Like
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy

def index(request):
    return render(request, "index.html")

class Home(LoginRequiredMixin, ListView):
    """HOMEページで、自分以外のユーザー投稿をリスト表示"""
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        #リクエストユーザーのみ除外
        return Post.objects.exclude(user=self.request.user)
   
class MyPost(LoginRequiredMixin, ListView):
    """自分の投稿のみ表示"""
    model = Post
    template_name = 'mypost.html'

    def get_queryset(self):
        #自分の投稿に限定
        return Post.objects.filter(user=self.request.user)

class OtherUserPostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'other_user_post_list.html'

    def get_queryset(self):
        return Post.objects.exclude(user=self.request.user)

class LikeCreate(LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        target = get_object_or_404(Post, pk=self.kwargs['pk'])
        Like.objects.create(target=target, user=self.request.user)
        return redirect('other_user_post_list', pk=self.request.user.pk)

class LikeDelete(DeleteView):
    model = Like

    def get_success_url(self):
        return redirect('other_user_post_list')