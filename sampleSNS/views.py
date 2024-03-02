from .models import Post
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
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
    template_name = 'list.html'

    def get_queryset(self):
        #自分の投稿に限定
        return Post.objects.filter(user=self.request.user)

class FollowList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list.html'